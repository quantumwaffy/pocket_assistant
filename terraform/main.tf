provider "aws" {
}

terraform {
  backend "s3" {}
}

module "ec2" {
  source          = "./modules/ec2"
  GITHUB_PAT      = var.GITHUB_PAT
  GITHUB_USERNAME = var.GITHUB_USERNAME
  GITHUB_REPO     = var.GITHUB_REPO
}
