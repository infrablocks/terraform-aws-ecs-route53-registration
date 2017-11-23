def cloud_watch_ecs_event_for(**kwargs):
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