import unittest
from unittest.mock import Mock

from ecs_route53_registration.ecs_container_instance import ECSContainerInstance
from ecs_route53_registration.ecs_task import ECSTask

from test.factories import \
    random_task_arn, \
    random_container_instance_arn, \
    random_cluster_arn


class TestECSTask(unittest.TestCase):
    def test_fetches_container_instance_for_task(self):
        ecs = Mock(name="ECS client")
        ec2 = Mock(name="EC2 client")
        logger = Mock(name="Logger")

        cluster_arn = random_cluster_arn()
        task_arn = random_task_arn()
        container_instance_arn = random_container_instance_arn()

        ecs.describe_tasks = Mock(
            name="Describe tasks",
            return_value={
                'tasks': [
                    {
                        'containerInstanceArn': container_instance_arn
                    }
                ]
            })

        ecs_task = ECSTask(cluster_arn, task_arn, ecs, ec2, logger)

        task_container_instance = ecs_task.container_instance()

        ecs.describe_tasks.assert_called_with(
            cluster=cluster_arn,
            tasks=[task_arn])

        self.assertEqual(
            task_container_instance,
            ECSContainerInstance(container_instance_arn, ecs, ec2, logger))
