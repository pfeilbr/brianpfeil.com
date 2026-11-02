# Live settings being written into Terraform; see ../imports.tf.

import {
  to = module.state_bucket.aws_s3_bucket_ownership_controls.state
  id = "brianpfeil-tfstate-529276214230"
}
