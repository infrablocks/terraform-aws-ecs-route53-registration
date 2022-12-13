module "ecs_route53_registration" {
  source = "./../../"

  region = var.region

  deployment_identifier = var.deployment_identifier

  cluster_arn = module.ecs_cluster.cluster_arn

  service_name = var.service_name

  hosted_zone_id = var.private_zone_id

  record_set_name_template = var.record_set_name_template
  record_set_ip_type = var.record_set_ip_type
}
