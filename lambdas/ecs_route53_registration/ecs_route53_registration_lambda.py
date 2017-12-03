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

    # if event corresponds to the service we are managing
    #   if event indicates a newly running task or
    #      event indicates a newly stopped task
    #     determine running tasks
    #     determine DNS name for each task
    #       fetch instance details
    #       populate DNS template
    #     add/update record in Route53
    # else
    #   ignore

    # types:
    #   CloudWatchECSEvent
    #     - tells us things about the received event
    #     - e.g., container instance ARN, cluster ARN, service name
    #     - actually may only need state change and service name since
    #       looking up the tasks should give container instance details
    #   ECSService
    #     - has many running ECSTasks
    #   ECSContainerInstance
    #     - tells us things about the container instance like IP address
    #   ECSTask
    #     - has many ECSContainerDefinitions
    #   ECSContainerDefinition
    #     - knows about what port the container listens on
    #