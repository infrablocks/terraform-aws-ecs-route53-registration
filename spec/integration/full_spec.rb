# frozen_string_literal: true

require 'spec_helper'

describe 'full' do
  let(:region) do
    var(role: :full, name: 'region')
  end
  let(:deployment_identifier) do
    var(role: :full, name: 'deployment_identifier')
  end
  let(:cluster_arn) do
    output(role: :full, name: 'cluster_arn')
  end
  let(:lambda_role_arn) do
    output(role: :full, name: 'lambda_role_arn')
  end
  let(:lambda_policy_arn) do
    output(role: :full, name: 'lambda_policy_arn')
  end

  before(:context) do
    apply(role: :full)
  end

  after(:context) do
    destroy(
      role: :full,
      only_if: -> { !ENV['FORCE_DESTROY'].nil? || ENV['SEED'].nil? }
    )
  end

  describe 'cluster task events rule' do
    subject(:cluster_task_event) do
      cloudwatch_event(
        "cluster-task-events-#{region}-#{deployment_identifier}"
      )
    end

    it { is_expected.to exist }

    its(:description) do
      is_expected.to eq(
        'All ECS task state change events for ' \
        "cluster: #{cluster_arn} (" \
        "region: #{region}, " \
        "deployment identifier: #{deployment_identifier})"
      )
    end

    it 'has an event pattern specifying events for the the provided cluster' do
      expect(JSON.parse(cluster_task_event.event_pattern))
        .to(eq({
                 'source' => ['aws.ecs'],
                 'detail-type' => ['ECS Task State Change'],
                 'detail' => {
                   'clusterArn' => [cluster_arn]
                 }
               }))
    end
  end

  describe 'cluster task events ECS Route53 registration target' do
    subject(:cluster_task_event_target) do
      cloudwatch_event_client
        .list_targets_by_rule(
          {
            rule: "cluster-task-events-#{region}-#{deployment_identifier}"
          }
        ).targets[0]
    end

    it 'points to the ARN of the ECS Route53 registration lambda function' do
      expect(cluster_task_event_target.arn)
        .to(eq(output(role: :full, name: 'lambda_arn')))
    end
  end

  describe 'IAM roles and policies' do
    describe 'ECS Route53 registration lambda role' do
      subject(:lambda_role) { iam_role(lambda_role_arn) }

      it { is_expected.to exist }
      it { is_expected.to have_iam_policy(lambda_policy_arn) }

      its(:description) do
        is_expected
          .to(eq('ECS Route53 registration lambda role (' \
                 "region: #{region}, " \
                 "deployment identifier: #{deployment_identifier})"))
      end

      it 'can be assumed by the lambda service' do
        expect(JSON.parse(CGI.unescape(
                            lambda_role.assume_role_policy_document
                          )))
          .to(include(
                {
                  'Statement' => [
                    {
                      'Sid' => '',
                      'Effect' => 'Allow',
                      'Action' => 'sts:AssumeRole',
                      'Principal' => {
                        'Service' => 'lambda.amazonaws.com'
                      }
                    }
                  ]
                }
              ))
      end
    end

    describe 'ECS Route53 registration lambda policy' do
      subject(:lambda_policy) { iam_policy(lambda_policy_arn) }

      let(:policy_document) do
        policy_version_response = iam_client.get_policy_version(
          {
            policy_arn: lambda_policy.arn,
            version_id: lambda_policy.default_version_id
          }
        )

        JSON.parse(CGI.unescape(
                     policy_version_response.policy_version.document
                   ))
      end

      it { is_expected.to exist }

      it 'has correct description' do
        expect(iam_client
                 .get_policy(policy_arn: lambda_policy_arn)
                 .policy.description)
          .to(eq('ECS Route53 registration lambda policy (' \
                 "region: #{region}, " \
                 "deployment identifier: #{deployment_identifier})"))
      end

      it 'allows logging' do
        expect(policy_document['Statement'])
          .to(include(
                {
                  'Sid' => '',
                  'Effect' => 'Allow',
                  'Action' => %w[
                    logs:PutLogEvents
                    logs:CreateLogStream
                    logs:CreateLogGroup
                  ],
                  'Resource' => '*'
                }
              ))
      end

      it 'allows ECS service lookup' do
        expect(policy_document['Statement'])
          .to(include(
                {
                  'Sid' => '',
                  'Effect' => 'Allow',
                  'Action' => %w[
                    ecs:ListTasks
                    ecs:DescribeTasks
                    ecs:DescribeContainerInstances
                    ec2:DescribeInstances
                  ],
                  'Resource' => '*'
                }
              ))
      end

      it 'allows Route53 record set management' do
        expect(policy_document['Statement'])
          .to(include(
                {
                  'Sid' => '',
                  'Effect' => 'Allow',
                  'Action' => %w[
                    route53:ListResourceRecordSets
                    route53:GetChange
                    route53:ChangeResourceRecordSets
                  ],
                  'Resource' => '*'
                }
              ))
      end
    end
  end

  describe 'lambdas' do
    describe 'ECS Route53 registration lambda' do
      subject(:route53_registration_lambda) do
        lambda(
          "ecs-route53-registration-lambda-#{region}-#{deployment_identifier}"
        )
      end

      its(:runtime) { is_expected.to(eq('python3.9')) }

      its(:handler) do
        is_expected.to(eq('ecs_route53_registration_lambda.amend_route53_for'))
      end

      its(:timeout) { is_expected.to(eq(300)) }

      its(:role) do
        is_expected.to(eq(output(role: :full, name: 'lambda_role_arn')))
      end

      it 'has correct environment' do
        expect(route53_registration_lambda.environment.variables)
          .to(eq({
                   'SERVICE_NAME' => var(role: :full, name: 'service_name'),
                   'HOSTED_ZONE_ID' => var(role: :full,
                                           name: 'private_zone_id'),
                   'RECORD_SET_NAME_TEMPLATE' =>
                     var(role: :full, name: 'record_set_name_template'),
                   'RECORD_SET_IP_TYPE' =>
                     var(role: :full, name: 'record_set_ip_type')
                 }))
      end
    end
  end
end
