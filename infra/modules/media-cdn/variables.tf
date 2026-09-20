variable "bucket_name" {
  description = "S3 bucket holding the media. No dots: a dotted name breaks TLS on the S3 origin."
  type        = string
}

variable "comment" {
  description = "Comment shown on the CloudFront distribution."
  type        = string
}

variable "description" {
  description = "Description on the origin access control."
  type        = string
}

variable "price_class" {
  description = "CloudFront price class. PriceClass_100 is North America and Europe only."
  type        = string
  default     = "PriceClass_100"
}
