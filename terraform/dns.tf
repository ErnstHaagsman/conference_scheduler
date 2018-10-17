data "aws_route53_zone" "main" {
  provider = "aws.aws-eu"
  name = "confsched.ernsthaagsman.com."
}

resource "aws_route53_record" "root" {
  provider = "aws.aws-eu"
  zone_id = "${data.aws_route53_zone.main.zone_id}"
  name = "${data.aws_route53_zone.main.name}"
  type = "A"
  ttl = "30"
  records = ["${aws_instance.web.public_ip}"]
}
