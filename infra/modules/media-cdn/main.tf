/**
 * media-cdn — a private S3 bucket fronted by CloudFront.
 *
 * The bucket has no public policy: only the distribution can read it, through
 * an origin access control, so direct S3 URLs return 403. Object names carry a
 * content hash (see tools/instagram-media), which is why the cache policy is
 * the fully-cached managed one.
 */

terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

# The managed CachingOptimized policy, looked up rather than hard-coded.
data "aws_cloudfront_cache_policy" "optimized" {
  name = "Managed-CachingOptimized"
}

# HSTS, X-Content-Type-Options: nosniff, X-Frame-Options, Referrer-Policy.
# nosniff is the one that matters most here: every file is served with the
# type S3 recorded, and the browser should not second-guess it.
data "aws_cloudfront_response_headers_policy" "security" {
  count = var.security_headers ? 1 : 0
  name  = "Managed-SecurityHeadersPolicy"
}

resource "aws_s3_bucket" "media" {
  bucket = var.bucket_name
  tags   = var.tags
}

resource "aws_s3_bucket_public_access_block" "media" {
  bucket = aws_s3_bucket.media.id

  block_public_acls  = true
  ignore_public_acls = true
  # The bucket policy below grants CloudFront read access, so policy-level
  # blocks stay off while ACL-level blocks stay on.
  block_public_policy     = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_server_side_encryption_configuration" "media" {
  bucket = aws_s3_bucket.media.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_cloudfront_origin_access_control" "media" {
  name = "${var.bucket_name}-oac"
  # Falls back to the distribution comment so a second instance needs only
  # bucket_name and comment.
  description                       = coalesce(var.description, var.comment)
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_distribution" "media" {
  enabled         = true
  comment         = var.comment
  tags            = var.tags
  price_class     = var.price_class
  http_version    = "http2and3"
  is_ipv6_enabled = true

  origin {
    domain_name              = aws_s3_bucket.media.bucket_regional_domain_name
    origin_id                = local.origin_id
    origin_access_control_id = aws_cloudfront_origin_access_control.media.id
  }

  default_cache_behavior {
    target_origin_id       = local.origin_id
    viewer_protocol_policy = "redirect-to-https"
    compress               = true
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    cache_policy_id        = data.aws_cloudfront_cache_policy.optimized.id

    response_headers_policy_id = var.security_headers ? data.aws_cloudfront_response_headers_policy.security[0].id : null
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}

# Attached after the distribution exists: the condition pins read access to
# this one distribution, so the ARN has to be known. Built with jsonencode
# rather than an aws_iam_policy_document data source: a data source is
# deferred whenever the distribution has any pending change, which made every
# CDN change also plan a (no-op) "bucket policy will be updated".
resource "aws_s3_bucket_policy" "media" {
  bucket = aws_s3_bucket.media.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid       = "AllowCloudFrontServicePrincipalReadOnly"
      Effect    = "Allow"
      Principal = { Service = "cloudfront.amazonaws.com" }
      Action    = "s3:GetObject"
      Resource  = "${aws_s3_bucket.media.arn}/*"
      Condition = {
        StringEquals = { "AWS:SourceArn" = aws_cloudfront_distribution.media.arn }
      }
    }]
  })
}

locals {
  origin_id = "s3-${var.bucket_name}"
}
