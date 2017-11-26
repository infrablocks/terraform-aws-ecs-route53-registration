module "ecs_route53_registration" {
  source = "../../../../"

  region = "${var.region}"

  deployment_identifier = "${var.deployment_identifier}"
}