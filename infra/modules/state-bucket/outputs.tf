output "bucket" {
  description = "State bucket name, for backend.hcl."
  value       = aws_s3_bucket.state.id
}

output "arn" {
  description = "State bucket ARN, for IAM policies that need to reach state."
  value       = aws_s3_bucket.state.arn
}
