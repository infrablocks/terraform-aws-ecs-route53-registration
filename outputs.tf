output "lambda_role_arn" {
  value = "${aws_iam_role.ecs_route53_registration_lambda_role.arn}"
}
