resource "aws_s3_bucket" "daily_backups" {
  bucket = "confsched-daily-backups"
  acl = "private"

  lifecycle_rule {
    enabled = true

    transition {
      days = 30
      storage_class = "STANDARD_IA"
    }
  }
}

resource "aws_s3_bucket" "hourly_backups" {
  bucket = "confsched-hourly-backups"
  acl = "private"

  lifecycle_rule {
    enabled = true

    expiration {
      days = 7
    }
  }
}
