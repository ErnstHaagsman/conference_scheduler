data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-bionic-18.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_key_pair" "key" {
  key_name = "confsched_key"
  public_key = "${file("~/.ssh/id_rsa.pub")}"
}

resource "aws_instance" "web" {
  ami = "${data.aws_ami.ubuntu.id}"
  instance_type = "t3.micro"
  availability_zone = "${var.default_az}"

  key_name = "${aws_key_pair.key.key_name}"

  vpc_security_group_ids = [
    "${aws_security_group.web_sg.id}"
  ]

  iam_instance_profile = "${aws_iam_instance_profile.web.name}"

  tags = {
    role = "web"
  }
}

resource "aws_ebs_volume" "db_volume" {
  availability_zone = "${var.default_az}"
  size = 4
  type = "gp2"
}

resource "aws_volume_attachment" "db_att" {
  device_name = "/dev/sdd"
  volume_id = "${aws_ebs_volume.db_volume.id}"
  instance_id = "${aws_instance.web.id}"
}

resource "aws_security_group" "web_sg" {
  name = "Security group for web boxes"

  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 80
    protocol = "tcp"
    to_port = 80
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 443
    protocol = "tcp"
    to_port = 443
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

