resource "aws_instance" "Amazon_Linux" {
  ami                    = "ami-04e601abe3e1a910f"
  instance_type          = "t2.micro"
  vpc_security_group_ids = [aws_security_group.ec2_security_group.id]
  user_data              = templatefile("./modules/ec2/ec2_boot.sh.tpl", {
    default_user         = var.EC2_DEFAULT_USER
  })
  key_name               = aws_key_pair.ec2_key_pair.key_name


  tags                   = {
    Name = "pocket_assistant"
  }
}

resource "aws_security_group" "ec2_security_group" {
  name = var.EC2_SECURITY_GROUP_NAME
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = var.EC2_SECURITY_GROUP_NAME
  }
}

resource "aws_key_pair" "ec2_key_pair" {
  key_name = var.EC2_SSH_KEY_NAME
  public_key = file(var.EC2_SSH_PUBLIC_KEY_PATH)
}

resource "null_resource" "ec2_provisioner" {
  depends_on = [aws_instance.Amazon_Linux]
  connection {
    type        = "ssh"
    user        = var.EC2_DEFAULT_USER
    host        = aws_instance.Amazon_Linux.public_ip
  }

  provisioner "remote-exec" {
    inline = [
      templatefile("./modules/ec2/ec2_github_runner.sh.tpl", {
    gh_pat      = var.GITHUB_PAT
    gh_username = var.GITHUB_USERNAME
    gh_repo     = var.GITHUB_REPO
  })
    ]
  }
}
