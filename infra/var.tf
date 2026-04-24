variable "env" {
  type = string
}

variable "prefix" {
  type = string
}

variable "location" {
  type = string
}
variable "min_replicas" {
  type        = number
  description = "Minimum number of replicas for the container app"
}
variable "subscription_id" {
  type      = string
  sensitive = true
}
