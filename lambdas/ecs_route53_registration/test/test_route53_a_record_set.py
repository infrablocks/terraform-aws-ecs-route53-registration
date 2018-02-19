import unittest

from unittest.mock import Mock
from datetime import datetime

from ecs_route53_registration.route53_a_record_set import Route53ARecordSet
from test.factories import \
    random_hosted_zone_id, \
    random_fqdn, \
    random_ip_address, \
    random_route53_change_id


class TestRoute53ARecordSet(unittest.TestCase):
    def test_upserts_record_set_when_at_least_one_ip_address_present(self):
        route53 = Mock(name='Route53 client')
        route53_waiter = Mock(name='Route53 Waiter')
        logger = Mock(name='Logger')

        change_id = random_route53_change_id()
        hosted_zone_id = random_hosted_zone_id()
        record_set_name = random_fqdn()
        ip_address_1 = random_ip_address()
        ip_address_2 = random_ip_address()
        ip_addresses = [
            ip_address_1,
            ip_address_2
        ]

        route53.change_resource_record_sets = Mock(
            name='Change resource record sets',
            return_value={
                'ChangeInfo': {
                    'Id': change_id,
                    'Status': 'PENDING',
                    'SubmittedAt': datetime(2017, 9, 1),
                    'Comment': 'Applying...'
                }
            })

        route53.get_waiter = Mock(
            name="Route53 waiter",
            return_value=route53_waiter)
        route53_waiter.wait = Mock(
            name="Route53 wait")

        route53_a_record_set = Route53ARecordSet(
            record_set_name, ip_addresses, route53, logger)

        route53_a_record_set.synchronise_with(hosted_zone_id)

        route53.change_resource_record_sets.assert_called_with(
            HostedZoneId=hosted_zone_id,
            ChangeBatch={
                'Comment': 'Managed by ECS Route53 registration lambda.',
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': record_set_name,
                            'Type': 'A',
                            'TTL': 60,
                            'ResourceRecords': [
                                {
                                    'Value': ip_address_1
                                },
                                {
                                    'Value': ip_address_2
                                }
                            ]
                        }
                    }
                ]
            })

        route53.get_waiter.assert_called_with(
            'resource_record_sets_changed')
        route53_waiter.wait.assert_called_with(
            Id=change_id,
            WaiterConfig={
                'Delay': 10,
                'MaxAttempts': 30
            })

    def test_deletes_record_set_when_no_ip_addresses_present(self):
        route53 = Mock(name='Route53 client')
        route53_waiter = Mock(name='Route53 Waiter')
        logger = Mock(name='Logger')

        change_id = random_route53_change_id()
        hosted_zone_id = random_hosted_zone_id()
        record_set_name = random_fqdn()
        old_ip_address_1 = random_ip_address()
        old_ip_address_2 = random_ip_address()
        new_ip_addresses = []

        route53.list_resource_record_sets = Mock(
            name='List resource record sets',
            return_value={
                'ResourceRecordSets': [
                    {
                        'Name': record_set_name,
                        'Type': 'A',
                        'ResourceRecords': [
                            {
                                'Value': old_ip_address_1
                            },
                            {
                                'Value': old_ip_address_2
                            }
                        ]
                    },
                ]
            })

        route53.change_resource_record_sets = Mock(
            name='Change resource record sets',
            return_value={
                'ChangeInfo': {
                    'Id': change_id,
                    'Status': 'PENDING',
                    'SubmittedAt': datetime(2017, 9, 1),
                    'Comment': 'Applying...'
                }
            })

        route53.get_waiter = Mock(
            name="Route53 waiter",
            return_value=route53_waiter)
        route53_waiter.wait = Mock(
            name="Route53 wait")

        route53_a_record_set = Route53ARecordSet(
            record_set_name, new_ip_addresses, route53, logger)

        route53_a_record_set.synchronise_with(hosted_zone_id)

        route53.change_resource_record_sets.assert_called_with(
            HostedZoneId=hosted_zone_id,
            ChangeBatch={
                'Comment': 'Managed by ECS Route53 registration lambda.',
                'Changes': [
                    {
                        'Action': 'DELETE',
                        'ResourceRecordSet': {
                            'Name': record_set_name,
                            'Type': 'A',
                            'TTL': 60,
                            'ResourceRecords': [
                                {
                                    'Value': old_ip_address_1
                                },
                                {
                                    'Value': old_ip_address_2
                                }
                            ]
                        }
                    }
                ]
            })

        route53.get_waiter.assert_called_with(
            'resource_record_sets_changed')
        route53_waiter.wait.assert_called_with(
            Id=change_id,
            WaiterConfig={
                'Delay': 10,
                'MaxAttempts': 30
            })

    def test_does_nothing_when_no_ip_addresses_present_and_no_record(self):
        route53 = Mock(name='Route53 client')
        logger = Mock(name='Logger')

        hosted_zone_id = random_hosted_zone_id()
        record_set_name = random_fqdn()
        ip_addresses = []

        route53.list_resource_record_sets = Mock(
            name='List resource record sets',
            return_value={
                'ResourceRecordSets': []
            })

        route53.change_resource_record_sets = Mock(
            name='Change resource record sets')
        route53.get_waiter = Mock(name="Route53 waiter")

        route53_a_record_set = Route53ARecordSet(
            record_set_name, ip_addresses, route53, logger)

        route53_a_record_set.synchronise_with(hosted_zone_id)

        route53.change_resource_record_sets.assert_not_called()
        route53.get_waiter.assert_not_called()
