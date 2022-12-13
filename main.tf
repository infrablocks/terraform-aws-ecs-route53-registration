data "archive_file" "ecs_route53_registration_lambda_contents" {
  type = "zip"
  source_dir = "${path.module}/lambdas/ecs_route53_registration"
  output_path = "${path.cwd}/build/ecs_route53_registration.zip"
}

resource "aws_lambda_function" "ecs_route53_registration" {
  function_name = "ecs-route53-registration-lambda-${var.region}-${var.deployment_identifier}"

  filename = data.archive_file.ecs_route53_registration_lambda_contents.output_path
  source_code_hash = data.archive_file.ecs_route53_registration_lambda_contents.output_base64sha256

  handler = "ecs_route53_registration_lambda.amend_route53_for"

  runtime = "python3.9"
  timeout = 300

  role = aws_iam_role.ecs_route53_registration_lambda_role.arn

  environment {
    variables = {
      SERVICE_NAME = var.service_name
      HOSTED_ZONE_ID = var.hosted_zone_id
      RECORD_SET_NAME_TEMPLATE = var.record_set_name_template
      RECORD_SET_IP_TYPE = var.record_set_ip_type
    }
  }
}
