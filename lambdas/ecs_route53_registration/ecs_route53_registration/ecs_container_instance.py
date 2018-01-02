class ECSContainerInstance(object):
    def __init__(
            self,
            cluster_arn,
            container_instance_arn,
            ecs,
            ec2,
            logger):
        self.cluster_arn = cluster_arn
        self.container_instance_arn = container_instance_arn
        self.ecs = ecs
        self.ec2 = ec2
        self.logger = logger

    def public_ip_address(self):
        return self._fetch()['PublicIpAddress']

    def private_ip_address(self):
        return self._fetch()['PrivateIpAddress']

    def _fetch(self):
        container_instances_response = \
            self.ecs.describe_container_instances(
                cluster=self.cluster_arn,
                containerInstances=[self.container_instance_arn])
        container_instance = \
            container_instances_response['containerInstances'][0]

        ec2_instance_id = container_instance['ec2InstanceId']

        ec2_instances_response = self.ec2.describe_instances(
            InstanceIds=[ec2_instance_id])
        ec2_instance = \
            ec2_instances_response['Reservations'][0]['Instances'][0]

        return ec2_instance

    def _to_dict(self):
        return {
            'cluster_arn': self.cluster_arn,
            'container_instance_arn': self.container_instance_arn,
        }

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._to_dict() == other._to_dict()
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted(self._to_dict().items())))

    def __repr__(self):
        return '<ECSContainerInstance %s> ' % str(self._to_dict())
