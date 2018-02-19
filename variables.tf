variable "region" {
  description = "The region into which the VPC auto peering lambda is being deployed."
}
variable "deployment_identifier" {
  description = "An identifier for this instantiation."
}

variable "cluster_arn" {
  description = "The ARN of the ECS cluster containing the service to be registered."
}

variable "service_name" {
  description = "The name of the service to register."
}
variable "hosted_zone_id" {
  description = "The ID of the hosted zone to register into."
}
variable "record_set_name_template" {
  description = "A template for the desired record set name."
}
variable "record_set_ip_type" {
  description = "The type of IP to use in the record set (\"public\" or \"private\")."
}
