# Live settings being written into Terraform. Each import adopts what is
# already there, so the plan shows an import and no change. Once applied, an
# import block is a no-op; it stays as a record of where the resource came from.

import {
  to = module.media_cdn.aws_s3_bucket_ownership_controls.media
  id = "brianpfeil-media01"
}
