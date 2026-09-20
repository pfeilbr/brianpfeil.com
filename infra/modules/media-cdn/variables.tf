variable "bucket_name" {
  description = "S3 bucket holding the media. Also names the origin and the OAC."
  type        = string

  validation {
    # A dotted name makes the S3 origin's certificate fail to match
    # *.s3.<region>.amazonaws.com, which breaks CloudFront's origin fetch.
    # This is why the bucket is brianpfeil-media01 and not com.brianpfeil.media01.
    condition     = !can(regex("\\.", var.bucket_name))
    error_message = "bucket_name must not contain dots: a dotted bucket breaks TLS on the S3 origin."
  }

  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$", var.bucket_name))
    error_message = "bucket_name must be a valid S3 bucket name: lowercase letters, digits and hyphens."
  }
}

variable "comment" {
  description = "Human-readable comment on the distribution, shown in the CloudFront console."
  type        = string
}

variable "description" {
  description = "Description on the origin access control."
  type        = string
  default     = null # falls back to the comment; see main.tf
}

variable "price_class" {
  description = "CloudFront price class. PriceClass_100 is North America and Europe only."
  type        = string
  default     = "PriceClass_100"

  validation {
    condition     = contains(["PriceClass_100", "PriceClass_200", "PriceClass_All"], var.price_class)
    error_message = "price_class must be PriceClass_100, PriceClass_200 or PriceClass_All."
  }
}

variable "tags" {
  description = "Extra tags for this instance, merged over the provider's default_tags."
  type        = map(string)
  default     = {}
}
