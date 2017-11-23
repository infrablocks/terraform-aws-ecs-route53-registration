import unittest

from test.factories import (cloud_watch_ecs_event_for)

from ecs_route53_registration.cloud_watch_ecs_event import CloudWatchECSEvent


class TestBasic(unittest.TestCase):
    def test_extracts_cluster_arn_from_event_detail(self):
        cluster_arn = 'arn:aws:ecs:eu-west-1:111122223333:cluster/some-cluster'
        event_content = cloud_watch_ecs_event_for(
            cluster_arn=cluster_arn)

        event = CloudWatchECSEvent(event_content)

        self.assertEqual(event.cluster_arn(), cluster_arn)

if __name__ == '__main__':
    unittest.main()
