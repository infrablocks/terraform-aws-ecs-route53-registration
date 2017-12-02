require 'spec_helper'

describe 'Lambdas' do
  include_context :terraform

  let(:region) {vars.region}
  let(:deployment_identifier) {vars.deployment_identifier}

  context 'ECS Route53 registration lambda' do
    subject {
      lambda("ecs-route53-registration-lambda-#{region}-#{deployment_identifier}")
    }

    its(:runtime) {should eq('python3.6')}
    its(:handler) {should eq('ecs_route53_registration_lambda.amend_route53_for')}
    its(:timeout) {should eq(300)}
    its(:role) do
      should eq(output_for(:harness, 'lambda_role_arn'))
    end
  end
end
