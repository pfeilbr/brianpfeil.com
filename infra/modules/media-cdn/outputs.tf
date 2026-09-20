output "bucket" {
  description = "Bucket name, for `aws s3 sync` in the publish step."
  value       = aws_s3_bucket.media.id
}

output "domain_name" {
  description = "CloudFront domain. This is base_url in tools/instagram-media/config.yaml."
  value       = aws_cloudfront_distribution.media.domain_name
}

output "distribution_id" {
  description = "Distribution id, for cache invalidations."
  value       = aws_cloudfront_distribution.media.id
}
