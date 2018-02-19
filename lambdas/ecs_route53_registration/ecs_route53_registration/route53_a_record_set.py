class Route53ARecordSet(object):
    def __init__(self, name, ip_addresses, route53, logger):
        self.name = name
        self.ip_addresses = ip_addresses
        self.route53 = route53
        self.logger = logger

    def synchronise_with(self, hosted_zone_id):
        self.logger.info(
            'Synchronising A record for: %s in Route53 hosted zone: %s '
            'with value(s): %s',
            self.name, hosted_zone_id, self.ip_addresses)

        if self.ip_addresses:
            self.logger.info(
                'IP addresses are present. Upserting record.')

            action = 'UPSERT'
            records = list({'Value': ip_address}
                           for ip_address in self.ip_addresses)
        else:
            self.logger.info(
                'IP addresses are missing. Deleting record.')

            action = 'DELETE'
            resource_record_sets_response = \
                self.route53.list_resource_record_sets(
                    HostedZoneId=hosted_zone_id,
                    StartRecordName=self.name,
                    StartRecordType='A')
            resource_record_sets = \
                resource_record_sets_response['ResourceRecordSets']

            self.logger.debug(
                'Found resource record sets: %s for hosted zone: %s '
                'and name: %s',
                resource_record_sets, hosted_zone_id, self.name)

            if resource_record_sets:
                records = resource_record_sets[0]['ResourceRecords']
            else:
                self.logger.info(
                    'Attempting to delete and no resource record set found '
                    'for: %s. Ignoring.', self.name)
                return

        self.logger.info(
            'Changing resource record set for: %s using action: %s with '
            'records: %s.',
            self.name, action, records)

        change_info_response = self.route53.change_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            ChangeBatch={
                'Comment': 'Managed by ECS Route53 registration lambda.',
                'Changes': [
                    {
                        'Action': action,
                        'ResourceRecordSet': {
                            'Name': self.name,
                            'Type': 'A',
                            'TTL': 60,
                            'ResourceRecords': records
                        }
                    }
                ]
            })
        change_info = change_info_response['ChangeInfo']

        self.logger.debug(
            'Change request for: %s resulted in: %s',
            self.name, change_info)

        wait_delay = 10
        wait_maximum_attempts = 30
        change_id = change_info['Id']

        self.logger.info(
            'Waiting for change with ID: %s to become effective with '
            'delay: %s and maximum attempts: %s.',
            change_id, wait_delay, wait_maximum_attempts)

        waiter = self.route53.get_waiter('resource_record_sets_changed')
        waiter.wait(
            Id=change_id,
            WaiterConfig={
                'Delay': wait_delay,
                'MaxAttempts': wait_maximum_attempts
            })

        self.logger.info(
            'Change with ID: %s successfully applied.', change_id)
