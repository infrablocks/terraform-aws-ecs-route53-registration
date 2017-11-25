import logging
import json

from ecs_route53_registration.cloud_watch_ecs_event import CloudWatchECSEvent

logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('boto3').setLevel(logging.CRITICAL)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def amend_route53_for(event, context):
    logger.debug('Processing event: %s', json.dumps(event))

    cloud_watch_ecs_event = CloudWatchECSEvent(event)

    logger.debug(
        'Event is for container instance with ARN: %s in cluster with ARN: %s',
        cloud_watch_ecs_event.container_instance_arn(),
        cloud_watch_ecs_event.cluster_arn())
