variable "env" {
  type = string
}

variable "prefix" {
  type = string
}

variable "region" {
  type    = string
  default = "us-east-1"
}

variable "desired_count" {
  type    = number
  default = 1
}

variable "domain_name" {
  type        = string
  description = "Custom domain this environment's ALB should serve, e.g. calcstaging.darojo.net"
}
