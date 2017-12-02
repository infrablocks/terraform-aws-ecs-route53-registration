data "aws_iam_policy_document" "ecs_route53_registration_assume_role_policy_document" {
  statement {
    effect = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      identifiers = ["lambda.amazonaws.com"]
      type = "Service"
    }
  }
}

data "aws_iam_policy_document" "ecs_route53_registration_lambda_role_policy_document" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]

    resources = ["*"]
  }
}

resource "aws_iam_role" "ecs_route53_registration_lambda_role" {
  description = "ECS Route53 registration lambda role (region: ${var.region}, deployment identifier: ${var.deployment_identifier})"
  assume_role_policy = "${data.aws_iam_policy_document.ecs_route53_registration_assume_role_policy_document.json}"
}

resource "aws_iam_policy" "ecs_route53_registration_lambda_role_policy" {
  description = "ECS Route53 registration lambda policy (region: ${var.region}, deployment identifier: ${var.deployment_identifier})"
  policy = "${data.aws_iam_policy_document.ecs_route53_registration_lambda_role_policy_document.json}"
}

resource "aws_iam_role_policy_attachment" "ecs_route53_registration_lambda_role_policy_attachment" {
  policy_arn = "${aws_iam_policy.ecs_route53_registration_lambda_role_policy.arn}"
  role = "${aws_iam_role.ecs_route53_registration_lambda_role.name}"
}
