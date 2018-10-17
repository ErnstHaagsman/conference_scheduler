provider "aws" {
  alias = "aws-eu"
  region = "eu-central-1"
}

provider "aws" {
  region = "us-west-2"
}
