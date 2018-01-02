from ecs_route53_registration.ecs_task import ECSTask


class ECSService(object):
    def __init__(
            self,
            cluster_arn,
            service_name,
            ecs,
            ec2,
            logger):
        self.cluster_arn = cluster_arn
        self.service_name = service_name
        self.ecs = ecs
        self.ec2 = ec2
        self.logger = logger

    def running_tasks(self):
        tasks_response = self.ecs.list_tasks(
            cluster=self.cluster_arn,
            serviceName=self.service_name)
        task_arns = tasks_response['taskArns']

        return list(
            ECSTask(
                self.cluster_arn,
                task_arn,
                self.ecs,
                self.ec2,
                self.logger)
            for task_arn in task_arns)
