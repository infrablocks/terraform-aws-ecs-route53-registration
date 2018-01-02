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

    def test_extracts_last_status_from_event_detail(self):
        last_status = 'PENDING'
        event_content = cloud_watch_ecs_event_content_for(
            last_status=last_status)

        event = CloudWatchECSEvent(event_content)

        self.assertEqual(event.last_status(), last_status)

    def test_extracts_desired_status_from_event_detail(self):
        desired_status = 'STOPPED'
        event_content = cloud_watch_ecs_event_content_for(
            desired_status=desired_status)

        event = CloudWatchECSEvent(event_content)

        self.assertEqual(event.desired_status(), desired_status)

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

    def test_represents_newly_running_task_when_last_status_running_and_current_status_running(self):
        last_status = 'RUNNING'
        desired_status = 'RUNNING'
        event_content = cloud_watch_ecs_event_content_for(
            last_status=last_status,
            desired_status=desired_status)

        event = CloudWatchECSEvent(event_content)

        self.assertTrue(event.represents_newly_running_task())

    def test_does_not_represent_newly_running_task_when_last_status_not_running_and_current_status_not_running(self):
        last_status = 'PENDING'
        desired_status = 'RUNNING'
        event_content = cloud_watch_ecs_event_content_for(
            last_status=last_status,
            desired_status=desired_status)

        event = CloudWatchECSEvent(event_content)

        self.assertFalse(event.represents_newly_running_task())

    def test_represents_newly_stopped_task_when_last_status_stopped_and_current_status_stopped(self):
        last_status = 'STOPPED'
        desired_status = 'STOPPED'
        event_content = cloud_watch_ecs_event_content_for(
            last_status=last_status,
            desired_status=desired_status)

        event = CloudWatchECSEvent(event_content)

        self.assertTrue(event.represents_newly_stopped_task())

    def test_does_not_represent_newly_stopped_task_when_last_status_not_stopped_and_current_status_not_stopped(self):
        last_status = 'RUNNING'
        desired_status = 'STOPPED'
        event_content = cloud_watch_ecs_event_content_for(
            last_status=last_status,
            desired_status=desired_status)

        event = CloudWatchECSEvent(event_content)

        self.assertFalse(event.represents_newly_stopped_task())

if __name__ == '__main__':
    unittest.main()
