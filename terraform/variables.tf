variable "GITHUB_PAT" {
  description = "GitHub personal access token to set up self-hosted runner"
  type        = string
}

variable "GITHUB_USERNAME" {
  description = "GitHub username to set up self-hosted runner"
  type        = string
}

variable "GITHUB_REPO" {
  description = "GitHub repository to set up self-hosted runner"
  type        = string
}

variable "EC2_DEFAULT_USER" {
  description = "Default user for chosen image"
  type        = string
  default     = "ec2-user"
}
