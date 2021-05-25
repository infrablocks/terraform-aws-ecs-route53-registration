resource "aws_iam_server_certificate" "service" {
  name = "wildcard-certificate-${var.component}-${var.deployment_identifier}"
  private_key = file(var.service_certificate_private_key)
  certificate_body = file(var.service_certificate_body)
}

module "base_network" {
  source = "infrablocks/base-networking/aws"
  version = "3.0.0"

  vpc_cidr = var.vpc_cidr
  region = var.region
  availability_zones = var.availability_zones

  component = var.component
  deployment_identifier = var.deployment_identifier

  private_zone_id = var.private_zone_id
}

module "ecs_cluster" {
  source = "infrablocks/ecs-cluster/aws"
  version = "3.5.0-rc.2"

  region = var.region
  vpc_id = module.base_network.vpc_id
  subnet_ids = module.base_network.private_subnet_ids
  allowed_cidrs = [var.private_network_cidr]

  component = var.component
  deployment_identifier = var.deployment_identifier

  cluster_name = var.cluster_name
  cluster_instance_ssh_public_key_path = var.cluster_instance_ssh_public_key_path
  cluster_instance_type = var.cluster_instance_type

  cluster_minimum_size = var.cluster_minimum_size
  cluster_maximum_size = var.cluster_maximum_size
  cluster_desired_capacity = var.cluster_desired_capacity
}

module "ecs_service" {
  source = "infrablocks/ecs-service/aws"
  version = "3.3.0-rc.1"

  component = var.component
  deployment_identifier = var.deployment_identifier

  region = var.region
  vpc_id = module.base_network.vpc_id

  service_task_container_definitions = var.service_task_container_definitions
  service_task_network_mode = var.service_task_network_mode

  service_name = var.service_name
  service_image = var.service_image
  service_command = var.service_command
  service_port = var.service_port

  service_desired_count = var.service_desired_count
  service_deployment_maximum_percent = var.service_deployment_maximum_percent
  service_deployment_minimum_healthy_percent = var.service_deployment_minimum_healthy_percent

  service_role = var.service_role
  service_volumes = var.service_volumes

  attach_to_load_balancer = var.attach_to_load_balancer

  ecs_cluster_id = module.ecs_cluster.cluster_id
  ecs_cluster_service_role_arn = module.ecs_cluster.service_role_arn
}
