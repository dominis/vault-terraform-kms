variable "download-url" {
  default     = "https://releases.hashicorp.com/vault/0.5.2/vault_0.5.2_linux_amd64.zip"
  description = "URL to download Vault"
}

variable "config" {
  description = "Configuration (text) for Vault"
}

variable "extra-install" {
  default     = ""
  description = "Extra commands to run in the install script"
}

variable "ami" {
  default     = "ami-7eb2a716"
  description = "AMI for Vault instances"
}

variable "availability-zones" {
  description = "Availabilizy zones for launcing the Vault instances"
}

variable "elb-health-check" {
  default     = "HTTP:8200/v1/sys/health"
  description = "Health check for Vault servers"
}

variable "instance_type" {
  default     = "t2.medium"
  description = "Instance type for Vault instances"
}

variable "key-name" {
  default     = "default"
  description = "SSH key name for Vault instances"
}

variable "nodes" {
  default     = "2"
  description = "number of Vault instances"
}

variable "subnets" {
  description = "list of subnets to launch Vault within"
}

variable "vpc-id" {
  description = "VPC ID"
}
