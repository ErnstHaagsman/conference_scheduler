data "aws_iam_policy_document" "backups_read_write" {
  statement {
    effect = "Allow"
    actions = [
      "s3:PutObject",
      "s3:GetObject"
    ]
    resources = [
      "${aws_s3_bucket.daily_backups.arn}/*",
      "${aws_s3_bucket.hourly_backups.arn}/*",
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "s3:ListBucket",
    ]
    resources = [
      "${aws_s3_bucket.daily_backups.arn}",
      "${aws_s3_bucket.hourly_backups.arn}",
    ]
  }
}

data "aws_iam_policy_document" "assume_ec2" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_policy" "backups_read_write" {
  name = "backups-rw"
  policy = "${data.aws_iam_policy_document.backups_read_write.json}"
}

resource "aws_iam_role" "web_role" {
  name = "web-role"
  assume_role_policy = "${data.aws_iam_policy_document.assume_ec2.json}"
}

resource "aws_iam_role_policy_attachment" "web_backups" {
  role = "${aws_iam_role.web_role.name}"
  policy_arn = "${aws_iam_policy.backups_read_write.arn}"
}

resource "aws_iam_instance_profile" "web" {
  name = "web"
  role = "${aws_iam_role.web_role.name}"
}
