import logging
import json
import boto3
import os

from string import Template

from ecs_route53_registration.validations import \
    ensure_present, \
    ensure_one_of
from ecs_route53_registration.cloud_watch_ecs_event import CloudWatchECSEvent
from ecs_route53_registration.ecs_service import ECSService

logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('boto3').setLevel(logging.CRITICAL)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def amend_route53_for(event, context):
    logger.debug('Processing event: %s', json.dumps(event))

    ecs = boto3.client('ecs')
    ec2 = boto3.client('ec2')

    service_name = ensure_present(
        os.environ['SERVICE_NAME'],
        'SERVICE_NAME must be provided.')
    hosted_zone_id = ensure_present(
        os.environ['HOSTED_ZONE_ID'],
        'HOSTED_ZONE_ID must be provided.')
    record_set_name_template = Template(ensure_present(
        os.environ['RECORD_SET_NAME_TEMPLATE'],
        'RECORD_SET_NAME_TEMPLATE must be provided.'))
    record_set_ip_type = ensure_one_of(
        ['public', 'private'],
        os.environ['RECORD_SET_IP_TYPE'],
        'RECORD_SET_IP_TYPE must be one of [\'public\', \'private\'].')

    cloud_watch_ecs_event = CloudWatchECSEvent(event)

    if cloud_watch_ecs_event.pertains_to_service(service_name):
        logger.info(
            'Event pertains to service %s. Continuing.', service_name)

        if cloud_watch_ecs_event.represents_possible_task_ip_change():
            logger.info(
                'Event represents possible task IP change. '
                'Refreshing Route53 records.')

            logger.info(
                'Determining %s IP address(es) for service.',
                record_set_ip_type)

            service = ECSService(
                cloud_watch_ecs_event.cluster_arn(),
                service_name,
                ecs, ec2, logger)
            tasks = service.running_tasks()
            container_instances = \
                (task.container_instance() for task in tasks)
            ip_addresses = \
                (container_instance['%s_ip' % record_set_ip_type]()
                 for container_instance in container_instances)

            logger.info(
                'Service has %s %s IP address(es): %s.',
                len(ip_addresses), record_set_ip_type, ip_addresses)

            logger.info(
                'Determining Route53 record set name using template: %s.',
                record_set_name_template.template)
            record_set_name = record_set_name_template.substitute({
                service_name: service_name,
                record_set_ip_type: record_set_ip_type
            })
            logger.info(
                'Service has Route53 record set name: %s.',
                record_set_name)

            logger.info(
                'Synchronising %s record to Route53 with %s IP address(es): %s '
                'for hosted zone: %s',
                record_set_name, record_set_ip_type, ip_addresses,
                hosted_zone_id)


            # if event corresponds to the service we are managing and
            #    (event indicates a newly running task or
            #     event indicates a newly stopped task)
            #   determine running tasks
            #   determine DNS name for each task
            #     fetch instance details
            #     populate DNS template
            #   upsert/delete record in Route53
            # else
            #   ignore

            # TASK_INTROSPECTION_NEEDED=("yes" or "no")
            # TASK_INTROSPECTION_PORT

            # make task introspection optional
            # communicate on private IP
            # collect instances that have the same resolved hostname
