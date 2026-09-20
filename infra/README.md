# infra

Terraform for the AWS side of brianpfeil.com. Every AWS resource here is
Terraform-managed; nothing is click-ops.

## Layout

```
infra/
├── backend.hcl              shared S3 backend settings (bucket named once)
├── backend.tf               site stack state key
├── main.tf                  site stack: the /media/ CDN
├── versions.tf
├── bootstrap/               creates the state bucket itself
│   ├── main.tf
│   └── backend.tf
├── modules/
│   ├── media-cdn/           private S3 bucket + CloudFront via OAC
│   └── state-bucket/        versioned, locked-down Terraform state bucket
└── scripts/
    └── fetch_provider.py    resumable provider download for slow links
```

The modules are the reusable units. A second CDN or a second state bucket is
another `module` block with a different name — nothing else to copy.

## State

Remote, in `s3://brianpfeil-tfstate-529276214230`:

| Stack | Key |
| --- | --- |
| `bootstrap/` | `bootstrap/terraform.tfstate` |
| `infra/` (site) | `site/terraform.tfstate` |

- **Locking** uses Terraform's native S3 lockfile (`use_lockfile`, Terraform
  ≥ 1.10) — there is no DynamoDB table.
- **Versioned**: every apply writes a new revision, so a bad apply can be
  rolled back to an earlier state object. Old revisions expire after 90 days,
  but the 20 most recent are always kept.
- Encrypted, all four public-access blocks on, TLS-only bucket policy, and
  `prevent_destroy` on the bucket.

`backend.hcl` holds the bucket, region and locking settings so they are
written exactly once; each stack's `backend.tf` declares only its key.

## Running it

```sh
aws sso login
make tf-init      # both stacks, against the S3 backend and local provider mirror
make tf-plan      # both stacks
make tf-validate
```

Apply from a saved plan, not `-auto-approve`:

```sh
cd infra
terraform plan -out=change.tfplan
terraform show change.tfplan     # read it
terraform apply change.tfplan
```

## The provider mirror

`terraform init` pulls ~174 MB of AWS provider from releases.hashicorp.com,
which has been unreliable from here (~50 KB/s, with long stalls). The
provider is installed once into `~/.terraform.d/plugin-mirror` and every init
uses `-plugin-dir` against it. On a fresh machine:

```sh
python3 infra/scripts/fetch_provider.py --detach
tail -f infra/.provider-cache/fetch.log
```

It resumes after interruptions, verifies the published SHA256, and runs
init / validate / plan when done. Because the mirror bypasses the registry,
the generated `.terraform.lock.hcl` only has darwin_arm64 hashes and is
gitignored rather than committed.

## Bootstrapping from nothing

Only needed if the state bucket itself is ever lost:

1. Delete `bootstrap/backend.tf` so the stack uses local state.
2. `cd infra/bootstrap && terraform init -plugin-dir=~/.terraform.d/plugin-mirror`
3. Plan to a file, read it, apply it — this recreates the bucket.
4. Restore `bootstrap/backend.tf`, then
   `terraform init -migrate-state -backend-config=../backend.hcl`.
5. Re-import the site stack's resources (ids are in `main.tf`'s outputs
   history and the AWS console), then `make tf-plan` should show no changes.

## History

The media bucket and distribution were first created with the AWS CLI while
building `/media/`, before the Terraform-only rule applied. They were adopted
with `import` blocks (plan: 6 to import, 0 to add, 0 to change, 0 to destroy)
and the blocks were removed once state was durable in S3.
