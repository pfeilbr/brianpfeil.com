terraform {
  required_version = ">= 1.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.region

  # On every taggable resource, so Cost Explorer and the tag editor can tell
  # this site's spend from the other projects in the account. Same keys as
  # the bootstrap stack's state bucket.
  default_tags {
    tags = {
      project    = "brianpfeil.com"
      managed-by = "terraform"
      stack      = "site"
    }
  }
}
