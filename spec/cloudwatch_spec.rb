require 'spec_helper'
require 'json'

describe 'CloudWatch' do
  include_context :terraform

  let(:region) {vars.region}
  let(:deployment_identifier) {vars.deployment_identifier}
  let(:cluster_arn) {output_for(:prerequisites, 'cluster_arn')}

  context 'cluster task events rule' do
    subject {
      cloudwatch_event(
          "cluster-task-events-#{region}-#{deployment_identifier}")
    }

    it {should exist}
    its(:description) {
      should eq(
                 "All ECS task state change events for " +
                     "cluster: #{cluster_arn} (" +
                     "region: #{region}, " +
                     "deployment identifier: #{deployment_identifier})")}

    it 'has an event pattern specifying events for the the provided cluster' do
      expect(JSON.parse(subject.event_pattern))
          .to(eq({
                     'source' => ['aws.ecs'],
                     'detail-type' => ['ECS Task State Change'],
                     'detail' => {
                         'clusterArn' => [cluster_arn]
                     }
                 }))
    end
  end

  context 'cluster task events ECS Route53 registration target' do
    subject {
      cloudwatch_events_client.list_targets_by_rule({
          rule: "cluster-task-events-#{region}-#{deployment_identifier}"
      }).targets[0]
    }

    it 'points to the ARN of the ECS Route53 registration lambda function' do
      expect(subject.arn).to(eq(output_for(:harness, 'lambda_arn')))
    end
  end
end
