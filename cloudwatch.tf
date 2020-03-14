data "template_file" "cluster_task_events_pattern" {
  template = file("${path.module}/templates/cluster-task-events-pattern.json.tpl")

  vars {
    cluster_arn = var.cluster_arn
  }
}

resource "aws_cloudwatch_event_rule" "cluster_task_events" {
  name = "cluster-task-events-${var.region}-${var.deployment_identifier}"
  description = "All ECS task state change events for cluster: ${var.cluster_arn} (region: ${var.region}, deployment identifier: ${var.deployment_identifier})"

  event_pattern = data.template_file.cluster_task_events_pattern.rendered
}

resource "aws_cloudwatch_event_target" "cluster_task_events_ecs_route53_registration_target" {
  rule = aws_cloudwatch_event_rule.cluster_task_events.name
  arn = aws_lambda_function.ecs_route53_registration.arn
}

resource "aws_lambda_permission" "cluster_task_events_ecs_route53_registration_invocation" {
  statement_id = "ecs-route53-registration-cluster-task-events-invocation"

  action = "lambda:InvokeFunction"
  principal = "events.amazonaws.com"

  source_arn = aws_cloudwatch_event_rule.cluster_task_events.arn
  function_name = aws_lambda_function.ecs_route53_registration.function_name
}
