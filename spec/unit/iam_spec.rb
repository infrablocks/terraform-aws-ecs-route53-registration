# frozen_string_literal: true

require 'spec_helper'

describe 'IAM' do
  let(:region) do
    var(role: :root, name: 'region')
  end
  let(:deployment_identifier) do
    var(role: :root, name: 'deployment_identifier')
  end

  describe 'by default' do
    before(:context) do
      @plan = plan(role: :root)
    end

    it 'creates an IAM role' do
      expect(@plan)
        .to(include_resource_creation(type: 'aws_iam_role')
              .once)
    end

    it 'includes the region and deployment identifier in the ' \
       'IAM role description' do
      expect(@plan)
        .to(include_resource_creation(type: 'aws_iam_role')
              .with_attribute_value(
                :description,
                including(region)
                  .and(including(deployment_identifier))
              ))
    end

    it 'allows the lambda service to assume the IAM role' do
      expect(@plan)
        .to(include_resource_creation(type: 'aws_iam_role')
              .with_attribute_value(
                :assume_role_policy,
                a_policy_with_statement(
                  Effect: 'Allow',
                  Action: 'sts:AssumeRole',
                  Principal: {
                    Service: 'lambda.amazonaws.com'
                  }
                )
              ))
    end

    it 'creates an IAM policy' do
      expect(@plan)
        .to(include_resource_creation(type: 'aws_iam_policy')
              .once)
    end

    it 'includes the region and deployment identifier in the ' \
       'IAM policy description' do
      expect(@plan)
        .to(include_resource_creation(type: 'aws_iam_policy')
              .with_attribute_value(
                :description,
                including(region)
                  .and(including(deployment_identifier))
              ))
    end

    it 'allows the execution role to manage logs' do
      expect(@plan)
        .to(include_resource_creation(type: 'aws_iam_policy')
              .with_attribute_value(
                :policy,
                a_policy_with_statement(
                  Effect: 'Allow',
                  Resource: '*',
                  Action: %w[
                    logs:CreateLogGroup
                    logs:CreateLogStream
                    logs:PutLogEvents
                  ]
                )
              ))
    end

    it 'allows the execution role to describe tasks' do
      expect(@plan)
        .to(include_resource_creation(type: 'aws_iam_policy')
              .with_attribute_value(
                :policy,
                a_policy_with_statement(
                  Effect: 'Allow',
                  Resource: '*',
                  Action: %w[
                    ecs:ListTasks
                    ecs:DescribeTasks
                    ecs:DescribeContainerInstances
                    ec2:DescribeInstances
                  ]
                )
              ))
    end

    it 'allows the execution role to manage record sets' do
      expect(@plan)
        .to(include_resource_creation(type: 'aws_iam_policy')
              .with_attribute_value(
                :policy,
                a_policy_with_statement(
                  Effect: 'Allow',
                  Resource: '*',
                  Action: %w[
                    route53:ListResourceRecordSets
                    route53:GetChange
                    route53:ChangeResourceRecordSets
                  ]
                )
              ))
    end

    it 'creates an IAM policy attachment' do
      expect(@plan)
        .to(include_resource_creation(
          type: 'aws_iam_role_policy_attachment'
        )
              .once)
    end
  end
end
