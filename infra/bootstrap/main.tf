# Creates the bucket every other stack keeps its state in.
#
# This is the one stack that has to exist before remote state does, so its
# first apply ran with local state. backend.tf was added afterwards and
# `terraform init -migrate-state` moved this stack's own state into the bucket
# it had just made. Since then it behaves like any other stack.

terraform {
  required_version = ">= 1.10"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

data "aws_caller_identity" "current" {}

module "state_bucket" {
  source = "../modules/state-bucket"

  bucket_name = "brianpfeil-tfstate-${data.aws_caller_identity.current.account_id}"
  tags = {
    project    = "brianpfeil.com"
    managed-by = "terraform"
    purpose    = "terraform-state"
  }
}

output "state_bucket" {
  value = module.state_bucket.bucket
}
