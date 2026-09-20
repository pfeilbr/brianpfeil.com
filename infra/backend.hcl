# Shared S3 backend settings. Each stack declares only its own `key`; this
# file carries everything else, so the bucket is named in exactly one place.
#
#   terraform init -backend-config=backend.hcl        (from infra/)
#   terraform init -backend-config=../backend.hcl     (from infra/bootstrap/)

bucket       = "brianpfeil-tfstate-529276214230"
region       = "us-east-1"
encrypt      = true
use_lockfile = true # native S3 locking; no DynamoDB table (Terraform >= 1.10)
