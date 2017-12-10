class CloudWatchECSEvent(object):
    def __init__(self, event):
        self.event = event

    def cluster_arn(self):
        return self.event['detail']['clusterArn']

    def container_instance_arn(self):
        return self.event['detail']['containerInstanceArn']

    def service_name(self):
        return self.event['detail']['group'].partition(':')[2]

    def pertains_to_service(self, service_name):
        return self.service_name() == service_name