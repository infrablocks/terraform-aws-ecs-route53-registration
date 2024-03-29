output "vpc_id" {
  value = module.base_network.vpc_id
}

output "vpc_cidr" {
  value = module.base_network.vpc_cidr
}

output "public_subnet_ids" {
  value = module.base_network.public_subnet_ids
}

output "private_subnet_ids" {
  value = module.base_network.private_subnet_ids
}

output "cluster_arn" {
  value = module.ecs_cluster.cluster_id
}

output "cluster_name" {
  value = module.ecs_cluster.cluster_name
}

output "autoscaling_group_name" {
  value = module.ecs_cluster.autoscaling_group_name
}

output "launch_configuration_name" {
  value = module.ecs_cluster.launch_configuration_name
}

output "instance_role_arn" {
  value = module.ecs_cluster.instance_role_arn
}

output "instance_role_id" {
  value = module.ecs_cluster.instance_role_id
}

output "service_role_arn" {
  value = module.ecs_cluster.service_role_arn
}

output "service_role_id" {
  value = module.ecs_cluster.service_role_id
}

output "lambda_arn" {
  value = module.ecs_route53_registration.lambda_arn
}

output "lambda_role_arn" {
  value = module.ecs_route53_registration.lambda_role_arn
}

output "lambda_policy_arn" {
  value = module.ecs_route53_registration.lambda_policy_arn
}
