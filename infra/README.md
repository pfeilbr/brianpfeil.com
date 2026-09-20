# infra

Terraform for the AWS side of brianpfeil.com. Nothing here is click-ops — but
the resources it describes were, briefly: the `/media/` bucket and CloudFront
distribution were created with the AWS CLI before this directory existed, so
`imports.tf` adopts them instead of rebuilding them.

## Status

**Not yet applied.** `terraform init` needs the AWS provider (~180 MB) and the
download from releases.hashicorp.com was running at ~50 KB/s when this was
written. The config is unvalidated against the provider schema until someone
runs:

```sh
cd infra
terraform init
terraform plan    # expect: 6 to import, 0 to add, 0 to change, 0 to destroy
terraform apply
```

If the plan proposes *changing* or *destroying* anything, stop — it means the
config here has drifted from what is live, and the live resources are serving
the media page.

Once applied, the `import` blocks are inert and can be deleted.

## What it describes

| Resource | Id |
| --- | --- |
| S3 bucket (private) | `brianpfeil-media01` |
| Origin access control | `E17O3POTYCS2VP` |
| CloudFront distribution | `E2U0TCXARHWOEF` (`dfalwjniugna7.cloudfront.net`) |

`modules/media-cdn` is the reusable piece: a private bucket readable only by
one CloudFront distribution through OAC. The bucket name deliberately has no
dots — a dotted name breaks TLS validation on an S3 origin.

State is local and gitignored. Moving it to S3 is worth doing before anyone
else runs this.
