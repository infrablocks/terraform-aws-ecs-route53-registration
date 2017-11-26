data "archive_file" "ecs_route53_registration_lambda_contents" {
  type = "zip"
  source_dir = "${path.module}/lambdas/ecs_route53_registration"
  output_path = "${path.cwd}/build/ecs_route53_registration.zip"
}

resource "aws_lambda_function" "ecs_route53_registration" {
  function_name = "ecs-route53-registration-lambda-${var.region}-${var.deployment_identifier}"

  filename = "${data.archive_file.ecs_route53_registration_lambda_contents.output_path}"
  source_code_hash = "${data.archive_file.ecs_route53_registration_lambda_contents.output_base64sha256}"

  handler = "ecs_route53_registration.amend_route53_for"

  runtime = "python3.6"
  timeout = 300

  role = "${aws_iam_role.ecs_route53_registration_lambda_role.arn}"
}