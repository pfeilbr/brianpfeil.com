# brianpfeil.com's DNS, moved from Hover to Route 53 (2026-10-11).
#
# Every record Hover served, copied as-is, so the move changes nothing that
# works today:
#   - the site: GitHub Pages at the apex (all four of GitHub's A/AAAA, where
#     Hover had one A) and www → pfeilbr.github.io
#   - mail: MX to SES inbound (support@ → S3, the `store-in-s3` receipt rule)
#     and SES's domain verification TXT
#   - Hover's leftovers (mail CNAME, old ACME challenges), a wildcard to the
#     site, and dev01, kept
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

# Read off Hover's DNS page (2026-10-11): three records no lookup by name finds.
resource "aws_route53_record" "wildcard" {
  zone_id = local.zone_id
  name    = "*.brianpfeil.com"
  type    = "A"
  ttl     = 300
  records = ["185.199.108.153"]
}

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
