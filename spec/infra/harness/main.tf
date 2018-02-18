data "terraform_remote_state" "prerequisites" {
  backend = "local"

  config {
    path = "${path.module}/../../../../state/prerequisites.tfstate"
  }
}

module "ecs_route53_registration" {
  source = "../../../../"

  region = "${var.region}"

  deployment_identifier = "${var.deployment_identifier}"

  cluster_arn = "${data.terraform_remote_state.prerequisites.cluster_arn}"
}