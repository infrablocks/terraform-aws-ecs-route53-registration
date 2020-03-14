output "lambda_arn" {
  description = "The ARN of the created ECS Route53 registration lambda."
  value = aws_lambda_function.ecs_route53_registration.arn
}

output "lambda_role_arn" {
  description = "The ARN of the created ECS Route53 registration lambda role."
  value = aws_iam_role.ecs_route53_registration_lambda_role.arn
}

output "lambda_policy_arn" {
  description = "The ARN of the created ECS Route53 registration lambda policy."
  value = aws_iam_policy.ecs_route53_registration_lambda_role_policy.arn
}
