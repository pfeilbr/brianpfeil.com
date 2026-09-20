# Infrastructure for brianpfeil.com.
#
# These resources were first created with the AWS CLI while building /media/;
# the import blocks in imports.tf adopt them, so `terraform plan` is a no-op
# rather than a rebuild. Everything from here on goes through Terraform.

variable "region" {
  description = "AWS region."
  type        = string
  default     = "us-east-1"
}

module "media_cdn" {
  source = "./modules/media-cdn"

  bucket_name = "brianpfeil-media01"
  comment     = "brianpfeil.com media (Instagram archive)"
  description = "OAC for brianpfeil.com media"
  price_class = "PriceClass_100"
}

output "media_bucket" {
  value = module.media_cdn.bucket
}

output "media_domain_name" {
  value = module.media_cdn.domain_name
}

output "media_distribution_id" {
  value = module.media_cdn.distribution_id
}
