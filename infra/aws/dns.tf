data "cloudflare_zone" "darojo" {
  filter = {
    name = "darojo.net"
  }
}

resource "aws_acm_certificate" "app" {
  domain_name       = var.domain_name
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

resource "cloudflare_dns_record" "cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.app.domain_validation_options : dvo.domain_name => {
      name    = dvo.resource_record_name
      type    = dvo.resource_record_type
      content = dvo.resource_record_value
    }
  }

  zone_id = data.cloudflare_zone.darojo.zone_id
  name    = each.value.name
  type    = each.value.type
  content = each.value.content
  ttl     = 60
  proxied = false
}

resource "aws_acm_certificate_validation" "app" {
  certificate_arn = aws_acm_certificate.app.arn
  validation_record_fqdns = [
    for dvo in aws_acm_certificate.app.domain_validation_options : dvo.resource_record_name
  ]

  depends_on = [cloudflare_dns_record.cert_validation]
}

# DNS-only (gray cloud) - client connects directly to the ALB, which
# terminates TLS itself using the ACM cert above.
resource "cloudflare_dns_record" "app" {
  zone_id = data.cloudflare_zone.darojo.zone_id
  name    = trimsuffix(var.domain_name, ".${data.cloudflare_zone.darojo.name}")
  type    = "CNAME"
  content = aws_lb.app.dns_name
  ttl     = 300
  proxied = false
}
