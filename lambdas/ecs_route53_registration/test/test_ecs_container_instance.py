import unittest
from unittest.mock import Mock

from ecs_route53_registration.ecs_container_instance import ECSContainerInstance

from test.factories import \
    random_ec2_instance_id, \
    random_ip_address, \
    random_cluster_arn, \
    random_container_instance_arn


class TestECSContainerInstance(unittest.TestCase):
    def test_determines_public_ip_of_container_instance(self):
        ecs = Mock(name="ECS client")
        ec2 = Mock(name="EC2 client")
        logger = Mock(name="Logger")

        ec2_instance_id = random_ec2_instance_id()
        public_ip_address = random_ip_address()
        cluster_arn = random_cluster_arn()
        container_instance_arn = random_container_instance_arn()

        ecs.describe_container_instances = Mock(
            name="Describe container instances",
            return_value={
                'containerInstances': [
                    {
                        'ec2InstanceId': ec2_instance_id
                    }
                ]
            })
        ec2.describe_instances = Mock(
            name="Describe instances",
            return_value={
                'Reservations': [
                    {
                        'Instances': [
                            {
                                'PublicIpAddress': public_ip_address
                            }
                        ]
                    }
                ]
            })

        container_instance = ECSContainerInstance(
            cluster_arn, container_instance_arn, ecs, ec2, logger)

        found_public_ip_address = container_instance.public_ip_address()

        ecs.describe_container_instances.assert_called_with(
            cluster=cluster_arn,
            containerInstances=[container_instance_arn])
        ec2.describe_instances.assert_called_with(
            InstanceIds=[ec2_instance_id])

        self.assertEqual(found_public_ip_address, public_ip_address)

    def test_determines_private_ip_of_container_instance(self):
        ecs = Mock(name="ECS client")
        ec2 = Mock(name="EC2 client")
        logger = Mock(name="Logger")

        ec2_instance_id = random_ec2_instance_id()
        private_ip_address = random_ip_address()
        cluster_arn = random_cluster_arn()
        container_instance_arn = random_container_instance_arn()

        ecs.describe_container_instances = Mock(
            name="Describe container instances",
            return_value={
                'containerInstances': [
                    {
                        'ec2InstanceId': ec2_instance_id
                    }
                ]
            })
        ec2.describe_instances = Mock(
            name="Describe instances",
            return_value={
                'Reservations': [
                    {
                        'Instances': [
                            {
                                'PrivateIpAddress': private_ip_address
                            }
                        ]
                    }
                ]
            })

        container_instance = ECSContainerInstance(
            cluster_arn, container_instance_arn, ecs, ec2, logger)

        found_private_ip_address = container_instance.private_ip_address()

        ecs.describe_container_instances.assert_called_with(
            cluster=cluster_arn,
            containerInstances=[container_instance_arn])
        ec2.describe_instances.assert_called_with(
            InstanceIds=[ec2_instance_id])

        self.assertEqual(found_private_ip_address, private_ip_address)
