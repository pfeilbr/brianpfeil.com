/**
 * state-bucket — an S3 bucket for Terraform remote state.
 *
 * Versioned, so a bad apply or a corrupted state file can be rolled back to
 * any earlier revision. Locking uses Terraform's native S3 lockfile
 * (use_lockfile, Terraform >= 1.10), so there is no DynamoDB table to pay for
 * or keep in sync.
 */

terraform {
  required_version = ">= 1.10"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

resource "aws_s3_bucket" "state" {
  bucket = var.bucket_name
  tags   = var.tags

  # Losing this bucket loses the record of what every stack owns. Terraform
  # refuses to plan its destruction; removing this line is the deliberate act.
  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "state" {
  bucket = aws_s3_bucket.state.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "state" {
  bucket = aws_s3_bucket.state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# State files hold resource ids and sometimes secrets; nothing about this
# bucket is ever public.
resource "aws_s3_bucket_public_access_block" "state" {
  bucket = aws_s3_bucket.state.id

  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_policy" "state" {
  bucket = aws_s3_bucket.state.id
  # jsonencode rather than a policy-document data source, which would be
  # deferred (and plan a no-op update) whenever the bucket has any change.
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid       = "DenyInsecureTransport"
      Effect    = "Deny"
      Principal = "*"
      Action    = "s3:*"
      Resource  = [aws_s3_bucket.state.arn, "${aws_s3_bucket.state.arn}/*"]
      Condition = { Bool = { "aws:SecureTransport" = "false" } }
    }]
  })

  # The public access block must be in place before a policy is attached.
  depends_on = [aws_s3_bucket_public_access_block.state]
}

# Every apply writes a new version. Keep a generous history for rollback, but
# don't pay to store every revision forever.
resource "aws_s3_bucket_lifecycle_configuration" "state" {
  bucket = aws_s3_bucket.state.id

  rule {
    id     = "expire-old-state-versions"
    status = "Enabled"

    filter {}

    noncurrent_version_expiration {
      noncurrent_days           = var.noncurrent_version_days
      newer_noncurrent_versions = var.keep_newer_versions
    }

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }

  # Lifecycle rules on a bucket without versioning enabled are rejected.
  depends_on = [aws_s3_bucket_versioning.state]
}
