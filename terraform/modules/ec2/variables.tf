variable "EC2_SSH_KEY_NAME" {
  description = "The SSH Key Name"
  type        = string
  default     = "ec2-key-name"
}

variable "EC2_SSH_PUBLIC_KEY_PATH" {
  description = "The local path to the SSH Public Key"
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

variable "EC2_SECURITY_GROUP_NAME" {
  description = "The Name of the EC2 Security Group"
  type        = string
  default     = "pocket_assistant_ec2_security_group"
}

variable "EC2_DEFAULT_USER" {
  description = "Default user for chosen image"
  type        = string
  default     = "ec2-user"
}

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
