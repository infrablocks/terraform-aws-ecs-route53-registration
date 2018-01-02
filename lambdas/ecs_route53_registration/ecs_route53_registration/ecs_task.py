from ecs_route53_registration.ecs_container_instance import ECSContainerInstance


class ECSTask(object):
    def __init__(self, cluster_arn, task_arn, ecs, ec2, logger):
        self.cluster_arn = cluster_arn
        self.task_arn = task_arn
        self.ecs = ecs
        self.ec2 = ec2
        self.logger = logger

    def container_instance(self):
        task = next(
            iter(self.ecs.describe_tasks(
                cluster=self.cluster_arn,
                tasks=[self.task_arn])['tasks']),
            None)
        container_instance_arn = task['containerInstanceArn']

        return ECSContainerInstance(
            self.cluster_arn,
            container_instance_arn,
            self.ecs,
            self.ec2,
            self.logger)

    def _to_dict(self):
        return {
            'cluster_arn': self.cluster_arn,
            'task_arn': self.task_arn
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
        return '<ECSTask %s>' % str(self._to_dict())
