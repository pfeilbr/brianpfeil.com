# Remote state for the site stack. Shared settings (bucket, region, locking)
# are in backend.hcl; the bucket itself is created by bootstrap/.
terraform {
  backend "s3" {
    key = "site/terraform.tfstate"
  }
}
