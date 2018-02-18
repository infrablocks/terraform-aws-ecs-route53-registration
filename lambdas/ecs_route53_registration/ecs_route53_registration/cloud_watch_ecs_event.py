class CloudWatchECSEvent(object):
    def __init__(self, event):
        self.event = event

    def cluster_arn(self):
        return self.event['detail']['clusterArn']

    def container_instance_arn(self):
        return self.event['detail']['containerInstanceArn']

    def service_name(self):
        return self.event['detail']['group'].partition(':')[2]

    def last_status(self):
        return self.event['detail']['lastStatus']

    def desired_status(self):
        return self.event['detail']['desiredStatus']

    def pertains_to_service(self, service_name):
        return self.service_name() == service_name

    def represents_newly_running_task(self):
        return self.last_status() == 'RUNNING' and \
               self.desired_status() == 'RUNNING'

    def represents_newly_stopped_task(self):
        return self.last_status() == 'STOPPED' and \
               self.desired_status() == 'STOPPED'

    def represents_possible_task_ip_change(self):
        return self.represents_newly_running_task() or \
            self.represents_newly_stopped_task()