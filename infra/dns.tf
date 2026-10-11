# brianpfeil.com's DNS, moved from Hover to Route 53 (2026-10-11).
#
# Every record Hover served, copied as-is, so the move changes nothing that
# works today:
#   - the site: GitHub Pages at the apex (all four of GitHub's A/AAAA, where
#     Hover had one A) and www → pfeilbr.github.io
#   - mail: MX to SES inbound (support@ → S3, the `store-in-s3` receipt rule)
#     and SES's domain verification TXT
#   - Hover's leftovers (mail CNAME, old ACME challenges) and dev01, kept
#     until the move is settled
# The zone does nothing until the registrar's nameservers point at it
# (output `brianpfeil_com_nameservers`).

resource "aws_route53_zone" "brianpfeil_com" {
  name    = "brianpfeil.com"
  comment = "brianpfeil.com (moved from Hover)"
}

locals {
  zone_id           = aws_route53_zone.brianpfeil_com.zone_id
  github_pages_a    = ["185.199.108.153", "185.199.109.153", "185.199.110.153", "185.199.111.153"]
  github_pages_aaaa = ["2606:50c0:8000::153", "2606:50c0:8001::153", "2606:50c0:8002::153", "2606:50c0:8003::153"]
}

resource "aws_route53_record" "apex_a" {
  zone_id = local.zone_id
  name    = "brianpfeil.com"
  type    = "A"
  ttl     = 300
  records = local.github_pages_a
}

resource "aws_route53_record" "apex_aaaa" {
  zone_id = local.zone_id
  name    = "brianpfeil.com"
  type    = "AAAA"
  ttl     = 300
  records = local.github_pages_aaaa
}

resource "aws_route53_record" "www" {
  zone_id = local.zone_id
  name    = "www.brianpfeil.com"
  type    = "CNAME"
  ttl     = 300
  records = ["pfeilbr.github.io"]
}

resource "aws_route53_record" "mx" {
  zone_id = local.zone_id
  name    = "brianpfeil.com"
  type    = "MX"
  ttl     = 300
  records = ["10 inbound-smtp.us-east-1.amazonaws.com"]
}

resource "aws_route53_record" "ses_verification" {
  zone_id = local.zone_id
  name    = "_amazonses.brianpfeil.com"
  type    = "TXT"
  ttl     = 300
  records = ["c8FVMa/MdX5iAogvhq97j3hCHe1tCyQY2V4xTSW4Ajs="]
}

resource "aws_route53_record" "hover_mail" {
  zone_id = local.zone_id
  name    = "mail.brianpfeil.com"
  type    = "CNAME"
  ttl     = 300
  records = ["mail.hover.com.cust.hostedemail.com"]
}

resource "aws_route53_record" "old_acme" {
  zone_id = local.zone_id
  name    = "_acme-challenge.brianpfeil.com"
  type    = "TXT"
  ttl     = 300
  records = ["fY4ZQeKjiyudWh4-Ye7tVUjrytZ8wxu6QeUcDqPKRxU"]
}

output "brianpfeil_com_zone_id" {
  value = aws_route53_zone.brianpfeil_com.zone_id
}

output "brianpfeil_com_nameservers" {
  value = aws_route53_zone.brianpfeil_com.name_servers
}

# Read off Hover's DNS page (2026-10-11): records no lookup by name finds.
# Hover's `*` wildcard (→ GitHub Pages) is deliberately NOT copied: it sent every
# unknown name, media.brianpfeil.com included while resolvers still asked
# Hover, to GitHub's *.github.io certificate — a browser warning, not a site.
resource "aws_route53_record" "dev01" {
  zone_id = local.zone_id
  name    = "dev01.brianpfeil.com"
  type    = "A"
  ttl     = 300
  records = ["52.73.206.205"]
}

resource "aws_route53_record" "old_acme_www" {
  zone_id = local.zone_id
  name    = "_acme-challenge.www.brianpfeil.com"
  type    = "TXT"
  ttl     = 300
  records = ["dkOTzcON4bTWX4Xt0ETvbM6U3Rv2WxqRHZy3u7olZvY"]
}

# One wildcard certificate for every app at <app>.brianpfeil.com (media,
# relhub, …), used by each app's CloudFront distribution. A wildcard on
# purpose: certificate-transparency logs then show *.brianpfeil.com and never
# the name of any one app.
resource "aws_acm_certificate" "apps" {
  domain_name       = "*.brianpfeil.com"
  validation_method = "DNS"
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "apps_validation" {
  zone_id         = local.zone_id
  name            = one(aws_acm_certificate.apps.domain_validation_options).resource_record_name
  type            = one(aws_acm_certificate.apps.domain_validation_options).resource_record_type
  ttl             = 60
  records         = [one(aws_acm_certificate.apps.domain_validation_options).resource_record_value]
  allow_overwrite = true
}

resource "aws_acm_certificate_validation" "apps" {
  certificate_arn         = aws_acm_certificate.apps.arn
  validation_record_fqdns = [aws_route53_record.apps_validation.fqdn]
}

output "apps_certificate_arn" {
  value = aws_acm_certificate_validation.apps.certificate_arn
}
