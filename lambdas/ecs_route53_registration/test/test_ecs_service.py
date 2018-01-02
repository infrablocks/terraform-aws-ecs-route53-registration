import unittest
from unittest.mock import Mock

from ecs_route53_registration.ecs_service import ECSService
from ecs_route53_registration.ecs_task import ECSTask

from test.factories import random_cluster_arn, random_service_name, \
    random_task_arn


class TestECSService(unittest.TestCase):
    def test_fetches_all_tasks_in_service(self):
        ecs = Mock(name="ECS client")
        ec2 = Mock(name="EC2 client")
        logger = Mock(name="Logger")

        cluster_arn = random_cluster_arn()
        service_name = random_service_name()
        task_arn_1 = random_task_arn()
        task_arn_2 = random_task_arn()

        ecs.list_tasks = Mock(
            name="List tasks",
            return_value={
                'taskArns': [
                    task_arn_1,
                    task_arn_2
                ]
            })

        ecs_service = ECSService(
            cluster_arn,
            service_name,
            ecs,
            ec2,
            logger)

        found_tasks = ecs_service.running_tasks()

        ecs.list_tasks.assert_called_with(
            cluster=cluster_arn,
            serviceName=service_name)

        self.assertEqual(
            found_tasks,
            [
                ECSTask(cluster_arn, task_arn_1, ecs, ec2, logger),
                ECSTask(cluster_arn, task_arn_2, ecs, ec2, logger)
            ])