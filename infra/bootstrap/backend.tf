# Added after the first apply, once the bucket this stack creates existed.
# Shared settings (bucket, region, locking) are in ../backend.hcl.
terraform {
  backend "s3" {
    key = "bootstrap/terraform.tfstate"
  }
}
