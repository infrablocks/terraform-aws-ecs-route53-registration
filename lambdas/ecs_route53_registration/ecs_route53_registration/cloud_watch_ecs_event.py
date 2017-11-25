class CloudWatchECSEvent(object):
    def __init__(self, event):
        self.event = event

    def cluster_arn(self):
        return self.event['detail']['clusterArn']

    def container_instance_arn(self):
        return self.event['detail']['containerInstanceArn']