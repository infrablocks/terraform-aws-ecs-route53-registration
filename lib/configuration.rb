require 'securerandom'
require 'open-uri'
require 'ostruct'

require_relative 'paths'
require_relative 'vars'
require_relative 'public_address'

class Configuration
  def initialize
    @random_deployment_identifier = SecureRandom.hex[0, 8]
  end

  def deployment_identifier
    deployment_identifier_for(OpenStruct.new)
  end

  def deployment_identifier_for(args)
    args.deployment_identifier ||
        ENV['DEPLOYMENT_IDENTIFIER'] ||
        @random_deployment_identifier
  end

  def work_directory
    'build'
  end

  def for(role, args = OpenStruct.new)
    self.send("#{role}_parameters_for", args)
  end

  def prerequisites_parameters_for(args)
    deployment_identifier = deployment_identifier_for(args)
    source_directory = 'spec/infra/prerequisites'
    configuration_directory = File.join(work_directory, source_directory)
    state_file = Paths.from_project_root_directory('prerequisites.tfstate')
    vars_template_file = ENV['PREREQUISITES_VARS_TEMPLATE_FILE'] ||
        Paths.from_project_root_directory('config/vars/prerequisites.yml.erb')

    module_parameters_for(
        deployment_identifier,
        source_directory,
        configuration_directory,
        state_file,
        vars_template_file)
  end

  def harness_parameters_for(args)
    deployment_identifier = deployment_identifier_for(args)
    source_directory = 'spec/infra/harness'
    configuration_directory = File.join(work_directory, source_directory)
    state_file = Paths.from_project_root_directory('harness.tfstate')
    vars_template_file = ENV['HARNESS_VARS_TEMPLATE_FILE'] ||
        Paths.from_project_root_directory('config/vars/harness.yml.erb')

    module_parameters_for(
        deployment_identifier,
        source_directory,
        configuration_directory,
        state_file,
        vars_template_file)
  end

  def module_parameters_for(
      deployment_identifier,
      source_directory,
      configuration_directory,
      state_file,
      vars_template_file)
    OpenStruct.new(
        {
            deployment_identifier: deployment_identifier,
            source_directory: source_directory,
            work_directory: work_directory,
            configuration_directory: configuration_directory,
            state_file: state_file,
            vars: Vars.load_from(vars_template_file, {
                project_directory: Paths.project_root_directory,
                public_ip: PublicAddress.as_ip_address,
                deployment_identifier: deployment_identifier
            })
        })
  end
end