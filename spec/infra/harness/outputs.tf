output "lambda_arn" {
  value = "${module.ecs_route53_registration.lambda_arn}"
}

output "lambda_role_arn" {
  value = "${module.ecs_route53_registration.lambda_role_arn}"
}