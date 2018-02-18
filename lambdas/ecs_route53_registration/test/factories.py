import random
import string
import socket
import struct


def random_string(characters, length=20):
    return ''.join(random.choice(characters)
                   for n in range(length))


def random_numeric_string(length=20):
    return random_string(
        string.digits,
        length)


def random_alphanumeric_string(length=20):
    return random_string(
        string.ascii_letters + string.digits,
        length)


def random_uppercase_alphanumeric_string(length=20):
    return random_string(
        string.ascii_uppercase + string.digits,
        length)


def random_hexadecimal_string(length=20):
    return random_string(
        string.digits + 'abcdef',
        length)


def random_uuid():
    return '%s-%s-%s-%s-%s' % \
           (random_hexadecimal_string(8),
            random_hexadecimal_string(4),
            random_hexadecimal_string(4),
            random_hexadecimal_string(4),
            random_hexadecimal_string(12))


def random_account_id():
    return random_numeric_string(length=12)


def random_cluster_arn():
    account_id = random_account_id()
    cluster_name = random_alphanumeric_string()

    return 'arn:aws:ecs:eu-west-1:%s:cluster/%s' % \
           (account_id, cluster_name)


def random_task_arn():
    account_id = random_account_id()
    task_id = random_uuid()

    return 'arn:aws:ecs:eu-west-1:%s:task/%s' % \
           (account_id, task_id)


def random_container_instance_arn():
    account_id = random_account_id()
    container_instance_id = random_uuid()

    return 'arn:aws:ecs:eu-west-1:%s:container-instance/%s' % \
           (account_id, container_instance_id)


def random_service_name():
    return random_alphanumeric_string()


def random_ec2_instance_id():
    return 'i-%s' % random_hexadecimal_string(length=17)


def random_route53_change_id():
    return random_hexadecimal_string(length=8)


def random_ip_address():
    return socket.inet_ntoa(
        struct.pack('>I', random.randint(1, 0xffffffff)))


def random_hosted_zone_id():
    return 'Z%s' % random_uppercase_alphanumeric_string(length=13)


def random_fqdn():
    return '%s.example.com' % random_hexadecimal_string(length=8)


def cloud_watch_ecs_event_content_for(**kwargs):
    cluster_arn = kwargs.get(
        'cluster_arn',
        'arn:aws:ecs:eu-west-1:111122223333:cluster/cluster')
    container_instance_arn = kwargs.get(
        'container_instance_arn',
        'arn:aws:ecs:eu-west-1:111122223333:container-instance/instance')
    group = kwargs.get('group', 'service:potatoes')
    containers = kwargs.get('containers', [])
    last_status = kwargs.get('last_status', 'PENDING')
    desired_status = kwargs.get('desired_status', 'RUNNING')

    return {
        'detail': {
            'clusterArn': cluster_arn,
            'containerInstanceArn': container_instance_arn,
            'group': group,
            'containers': containers,
            'desiredStatus': desired_status,
            'lastStatus': last_status
        }
    }
