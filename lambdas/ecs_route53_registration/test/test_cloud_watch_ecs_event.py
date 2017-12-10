import unittest

from test.factories import (cloud_watch_ecs_event_content_for)

from ecs_route53_registration.cloud_watch_ecs_event import CloudWatchECSEvent


class TestBasic(unittest.TestCase):
    def test_extracts_cluster_arn_from_event_detail(self):
        cluster_arn = 'arn:aws:ecs:eu-west-1:111122223333:cluster/some-cluster'
        event_content = cloud_watch_ecs_event_content_for(
            cluster_arn=cluster_arn)

        event = CloudWatchECSEvent(event_content)

        self.assertEqual(event.cluster_arn(), cluster_arn)

    def test_extracts_container_instance_arn_from_event_detail(self):
        container_instance_arn = \
            'arn:aws:ecs:eu-west-1:111122223333:container-instance/some' \
            '-instance'
        event_content = cloud_watch_ecs_event_content_for(
            container_instance_arn=container_instance_arn)

        event = CloudWatchECSEvent(event_content)

        self.assertEqual(
            event.container_instance_arn(),
            container_instance_arn)

    def test_extracts_service_name_from_event_detail(self):
        service_name = 'some-service'
        event_content = cloud_watch_ecs_event_content_for(
            group='service:%s' % service_name)

        event = CloudWatchECSEvent(event_content)

        self.assertEqual(
            event.service_name(),
            service_name)

    def test_is_for_service_if_service_name_matches(self):
        target_service = 'target-service'
        event_content = cloud_watch_ecs_event_content_for(
            group='service:%s' % target_service)

        event = CloudWatchECSEvent(event_content)

        self.assertTrue(event.pertains_to_service(target_service))

    def test_is_not_for_service_if_service_name_does_not_match(self):
        target_service = 'target-service'
        different_service = 'different-service'
        event_content = cloud_watch_ecs_event_content_for(
            group='service:%s' % different_service)

        event = CloudWatchECSEvent(event_content)

        self.assertFalse(event.pertains_to_service(target_service))

if __name__ == '__main__':
    unittest.main()
