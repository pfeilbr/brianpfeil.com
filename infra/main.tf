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

# A second CDN (another site, another kind of media) is another block like
# this one with a different bucket_name — everything else has a default.
module "media_cdn" {
  source = "./modules/media-cdn"

  bucket_name = "brianpfeil-media01"
  comment     = "brianpfeil.com media (Instagram archive)"

  # Passed explicitly rather than defaulted from comment: it is what the live
  # OAC already says, and keeping it identical is what makes the import a
  # no-op instead of a change.
  description = "OAC for brianpfeil.com media"
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
