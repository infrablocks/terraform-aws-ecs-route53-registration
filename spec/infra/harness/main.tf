data "terraform_remote_state" "prerequisites" {
  backend = "local"

  config = {
    path = "${path.module}/../../../../state/prerequisites.tfstate"
  }
}

module "ecs_route53_registration" {
  # This makes absolutely no sense. I think there's a bug in terraform.
  source = "./../../../../../../../"

  region = var.region

  deployment_identifier = var.deployment_identifier

  cluster_arn = data.terraform_remote_state.prerequisites.outputs.cluster_arn

  service_name = var.service_name
  hosted_zone_id = var.hosted_zone_id
  record_set_name_template = var.record_set_name_template
  record_set_ip_type = var.record_set_ip_type
}
