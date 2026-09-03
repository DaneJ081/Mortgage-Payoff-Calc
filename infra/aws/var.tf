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
