# Adopts the resources that were created with the CLI before this existed.
# Once `terraform apply` has run once and state holds them, these blocks are
# inert and can be deleted.

import {
  to = module.media_cdn.aws_s3_bucket.media
  id = "brianpfeil-media01"
}

import {
  to = module.media_cdn.aws_s3_bucket_public_access_block.media
  id = "brianpfeil-media01"
}

import {
  to = module.media_cdn.aws_s3_bucket_server_side_encryption_configuration.media
  id = "brianpfeil-media01"
}

import {
  to = module.media_cdn.aws_s3_bucket_policy.media
  id = "brianpfeil-media01"
}

import {
  to = module.media_cdn.aws_cloudfront_origin_access_control.media
  id = "E17O3POTYCS2VP"
}

import {
  to = module.media_cdn.aws_cloudfront_distribution.media
  id = "E2U0TCXARHWOEF"
}
