output "lambda_arn" {
  value = "${aws_lambda_function.ecs_route53_registration.arn}"
}

output "lambda_role_arn" {
  value = "${aws_iam_role.ecs_route53_registration_lambda_role.arn}"
}

output "lambda_policy_arn" {
  value = "${aws_iam_policy.ecs_route53_registration_lambda_role_policy.arn}"
}
