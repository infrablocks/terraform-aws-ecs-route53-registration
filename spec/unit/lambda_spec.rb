# frozen_string_literal: true

require 'spec_helper'

describe 'lambda' do
  let(:region) do
    var(role: :root, name: 'region')
  end
  let(:deployment_identifier) do
    var(role: :root, name: 'deployment_identifier')
  end
  let(:service_name) do
    var(role: :root, name: 'service_name')
  end
  let(:hosted_zone_id) do
    var(role: :root, name: 'hosted_zone_id')
  end
  let(:record_set_name_template) do
    var(role: :root, name: 'record_set_name_template')
  end
  let(:record_set_ip_type) do
    var(role: :root, name: 'record_set_ip_type')
  end

  describe 'by default' do
    before(:context) do
      @plan = plan(role: :root)
    end

    it 'creates a lambda function' do
      expect(@plan)
        .to(include_resource_creation(type: 'aws_lambda_function')
              .once)
    end

    it 'includes the region and deployment identifier in the lambda ' \
       'function name' do
      expect(@plan)
        .to(include_resource_creation(type: 'aws_lambda_function')
              .with_attribute_value(
                :function_name,
                including(region).and(including(deployment_identifier))
              ))
    end

    it 'uses a handler of "vpc_auto_peering_lambda.peer_vpcs_for"' do
      expect(@plan)
        .to(include_resource_creation(type: 'aws_lambda_function')
              .with_attribute_value(
                :handler,
                'ecs_route53_registration_lambda.amend_route53_for'
              ))
    end

    it 'uses a runtime of "python3.9"' do
      expect(@plan)
        .to(include_resource_creation(type: 'aws_lambda_function')
              .with_attribute_value(:runtime, 'python3.9'))
    end

    it 'uses a timeout of 300 seconds' do
      expect(@plan)
        .to(include_resource_creation(type: 'aws_lambda_function')
              .with_attribute_value(:timeout, 300))
    end

    it 'includes a SERVICE_NAME environment variable with the ' \
       'provided service name as value' do
      expect(@plan)
        .to(include_resource_creation(type: 'aws_lambda_function')
              .with_attribute_value(
                [:environment, 0, :variables],
                a_hash_including(SERVICE_NAME: service_name)
              ))
    end

    it 'includes an HOSTED_ZONE_ID environment variable with the ' \
       'provided hosted zone ID as value' do
      expect(@plan)
        .to(include_resource_creation(type: 'aws_lambda_function')
              .with_attribute_value(
                [:environment, 0, :variables],
                a_hash_including(HOSTED_ZONE_ID: hosted_zone_id)
              ))
    end

    it 'includes a RECORD_SET_NAME_TEMPLATE environment variable with the ' \
       'provided record set name template as value' do
      expect(@plan)
        .to(include_resource_creation(type: 'aws_lambda_function')
              .with_attribute_value(
                [:environment, 0, :variables],
                a_hash_including(
                  RECORD_SET_NAME_TEMPLATE: record_set_name_template
                )
              ))
    end

    it 'includes a RECORD_SET_IP_TYPE environment variable with the ' \
       'provided record set IP type as value' do
      expect(@plan)
        .to(include_resource_creation(type: 'aws_lambda_function')
              .with_attribute_value(
                [:environment, 0, :variables],
                a_hash_including(
                  RECORD_SET_IP_TYPE: record_set_ip_type
                )
              ))
    end
  end
end
