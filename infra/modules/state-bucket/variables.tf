variable "bucket_name" {
  description = "Name of the state bucket. Globally unique; the account id suffix keeps it that way."
  type        = string

  validation {
    condition     = !can(regex("\\.", var.bucket_name))
    error_message = "bucket_name must not contain dots: a dotted bucket breaks TLS on virtual-hosted S3 URLs."
  }

  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$", var.bucket_name))
    error_message = "bucket_name must be a valid S3 bucket name: lowercase letters, digits and hyphens."
  }
}

variable "noncurrent_version_days" {
  description = "Days an old state revision is kept after being superseded."
  type        = number
  default     = 90

  validation {
    condition     = var.noncurrent_version_days >= 1
    error_message = "noncurrent_version_days must be at least 1."
  }
}

variable "keep_newer_versions" {
  description = "Old revisions always kept regardless of age, so a rollback target always exists."
  type        = number
  default     = 20
}

variable "tags" {
  description = "Tags for the bucket."
  type        = map(string)
  default     = {}
}
