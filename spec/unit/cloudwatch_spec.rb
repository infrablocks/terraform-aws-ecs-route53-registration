# frozen_string_literal: true

require 'spec_helper'

describe 'CloudWatch' do
  let(:region) do
    var(role: :root, name: 'region')
  end
  let(:deployment_identifier) do
    var(role: :root, name: 'deployment_identifier')
  end
  let(:cluster_arn) do
    output(role: :prerequisites, name: 'cluster_arn')
  end

  describe 'by default' do
    before(:context) do
      @plan = plan(role: :root)
    end

    it 'creates a CloudWatch event rule' do
      expect(@plan)
        .to(include_resource_creation(type: 'aws_cloudwatch_event_rule')
              .once)
    end

    it 'includes the region and deployment identifier in the rule name' do
      expect(@plan)
        .to(include_resource_creation(type: 'aws_cloudwatch_event_rule')
              .with_attribute_value(
                :name,
                including(region)
                  .and(including(deployment_identifier))
              ))
    end

    it 'includes the region, cluster ARN and deployment identifier in the ' \
       'rule description' do
      expect(@plan)
        .to(include_resource_creation(type: 'aws_cloudwatch_event_rule')
              .with_attribute_value(
                :description,
                including(region)
                  .and(including(cluster_arn))
                  .and(including(deployment_identifier))
              ))
    end

    it 'creates a Cloudwatch event target' do
      expect(@plan)
        .to(include_resource_creation(type: 'aws_cloudwatch_event_target')
              .once)
    end

    it 'creates a lambda permission' do
      expect(@plan)
        .to(include_resource_creation(type: 'aws_lambda_permission')
              .once)
    end

    it 'allows the registration lambda to be invoked by the CloudWatch ' \
       'events service' do
      expect(@plan)
        .to(include_resource_creation(type: 'aws_lambda_permission')
              .with_attribute_value(:action, 'lambda:InvokeFunction')
              .with_attribute_value(:principal, 'events.amazonaws.com'))
    end
  end
end
