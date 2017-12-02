require 'spec_helper'
require 'json'

describe 'IAM roles and policies' do
  include_context :terraform

  let(:region) {vars.region}
  let(:deployment_identifier) {vars.deployment_identifier}

  let(:lambda_role_arn) {output_for(:harness, 'lambda_role_arn')}
  let(:lambda_policy_arn) {output_for(:harness, 'lambda_policy_arn')}

  context 'ECS Route53 registration lambda role' do
    subject {iam_role(lambda_role_arn)}

    it {should exist}
    it {should have_iam_policy(lambda_policy_arn)}
    its(:description) {
      should eq('ECS Route53 registration lambda role (' +
                    "region: #{region}, " +
                    "deployment identifier: #{deployment_identifier})")}

    it 'can be assumed by the lambda service' do
      expect(JSON.parse(URI.decode(subject.assume_role_policy_document)))
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

  context 'ECS Route53 registration lambda policy' do
    subject {iam_policy(lambda_policy_arn)}

    let(:policy_document) do
      policy_version_response = iam_client.get_policy_version(
          {
              policy_arn: subject.arn,
              version_id: subject.default_version_id,
          })

      JSON.parse(URI.decode(
          policy_version_response.policy_version.document))
    end

    it {should exist}

    it 'has correct description' do
      expect(iam_client
                 .get_policy(policy_arn: lambda_policy_arn)
                 .policy.description)
          .to(eq('ECS Route53 registration lambda policy (' +
                     "region: #{region}, " +
                     "deployment identifier: #{deployment_identifier})"))
    end

    it 'allows logging' do
      expect(policy_document['Statement'])
          .to(include(
                  {
                      'Sid' => '',
                      'Effect' => 'Allow',
                      'Action' => [
                          'logs:PutLogEvents',
                          'logs:CreateLogStream',
                          'logs:CreateLogGroup'
                      ],
                      'Resource' => '*'
                  }))
    end
  end
end