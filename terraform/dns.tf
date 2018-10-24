data "aws_route53_zone" "main" {
  name = "confsched.ernsthaagsman.com."
}

resource "aws_route53_record" "root" {
  zone_id = "${data.aws_route53_zone.main.zone_id}"
  name = "${data.aws_route53_zone.main.name}"
  type = "A"
  ttl = "30"
  records = ["${aws_instance.web.public_ip}"]
}

resource "aws_route53_record" "test" {
  zone_id = "${data.aws_route53_zone.main.zone_id}"
  name = "test.${data.aws_route53_zone.main.name}"
  type = "A"
  ttl = "30"
  records = ["${aws_instance.web.public_ip}"]
}

resource "aws_route53_record" "staging" {
  zone_id = "${data.aws_route53_zone.main.zone_id}"
  name = "staging.${data.aws_route53_zone.main.name}"
  type = "A"
  ttl = "30"
  records = ["${aws_instance.web.public_ip}"]
}
