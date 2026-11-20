# apps.brianpfeil.com: a directory of every app in data/apps.json (2026-11-20).
#
# The page is built by Hugo with the rest of the site
# (layouts/partials/apps-portal.html → /apps-home/index.html, one
# self-contained file) and deployed with it to GitHub Pages. This
# distribution serves it under its own name: origin brianpfeil.com with
# origin path /apps-home, so every site deploy updates it and nothing here
# needs credentials in CI. CloudFront sends Host: brianpfeil.com to the
# origin, which is the name GitHub Pages serves.
#
# The viewer function keeps the subdomain to one page:
#   /  and /index.html      → the directory
#   /<key> or /<key>/       → 302 to brianpfeil.com/apps/<key>/, the app's short link
#   anything else           → 302 to /
#
# Certificate: the *.brianpfeil.com wildcard in dns.tf.

resource "aws_cloudfront_function" "apps_portal" {
  name    = "apps-brianpfeil-com-viewer"
  runtime = "cloudfront-js-2.0"
  comment = "apps.brianpfeil.com: / is the directory, /<key> goes to the app"
  publish = true
  code    = <<-JS
    function handler(event) {
      var uri = event.request.uri;
      if (uri === "/" || uri === "/index.html") {
        return event.request;
      }
      var m = uri.match(/^\/([a-z0-9]+(?:-[a-z0-9]+)*)\/?$/);
      var to = m ? "https://brianpfeil.com/apps/" + m[1] + "/" : "/";
      return {
        statusCode: 302,
        statusDescription: "Found",
        headers: { location: { value: to }, "cache-control": { value: "max-age=300" } }
      };
    }
  JS
}

data "aws_cloudfront_cache_policy" "caching_optimized" {
  name = "Managed-CachingOptimized"
}

data "aws_cloudfront_response_headers_policy" "security_headers" {
  name = "Managed-SecurityHeadersPolicy"
}

resource "aws_cloudfront_distribution" "apps_portal" {
  enabled             = true
  comment             = "apps.brianpfeil.com (directory of apps, from brianpfeil.com/apps-home/)"
  aliases             = ["apps.brianpfeil.com"]
  price_class         = "PriceClass_100"
  http_version        = "http2and3"
  is_ipv6_enabled     = true
  default_root_object = "index.html"

  origin {
    domain_name = "brianpfeil.com"
    origin_id   = "github-pages"
    origin_path = "/apps-home"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  default_cache_behavior {
    target_origin_id       = "github-pages"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    compress               = true
    # Honours GitHub Pages' Cache-Control (max-age=600), so a site deploy
    # shows here within ten minutes without an invalidation.
    cache_policy_id            = data.aws_cloudfront_cache_policy.caching_optimized.id
    response_headers_policy_id = data.aws_cloudfront_response_headers_policy.security_headers.id

    function_association {
      event_type   = "viewer-request"
      function_arn = aws_cloudfront_function.apps_portal.arn
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate_validation.apps.certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }
}

resource "aws_route53_record" "apps_a" {
  zone_id = local.zone_id
  name    = "apps.brianpfeil.com"
  type    = "A"
  alias {
    name                   = aws_cloudfront_distribution.apps_portal.domain_name
    zone_id                = aws_cloudfront_distribution.apps_portal.hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "apps_aaaa" {
  zone_id = local.zone_id
  name    = "apps.brianpfeil.com"
  type    = "AAAA"
  alias {
    name                   = aws_cloudfront_distribution.apps_portal.domain_name
    zone_id                = aws_cloudfront_distribution.apps_portal.hosted_zone_id
    evaluate_target_health = false
  }
}

output "apps_portal_distribution_id" {
  value = aws_cloudfront_distribution.apps_portal.id
}
