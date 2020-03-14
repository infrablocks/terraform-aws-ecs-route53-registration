require 'rspec/core/rake_task'
require 'securerandom'
require 'git'
require 'semantic'
require 'rake_terraform'

require_relative 'lib/configuration'
require_relative 'lib/version'

configuration = Configuration.new

def repo
  Git.open('.')
end

def latest_tag
  repo.tags.map do |tag|
    Semantic::Version.new(tag.name)
  end.max
end

RakeTerraform.define_installation_tasks(
    path: File.join(Dir.pwd, 'vendor', 'terraform'),
    version: '0.12.19')

task :default => 'test:all'

namespace :virtualenv do
  desc "Create virtualenv."
  task :create do
    mkdir_p 'vendor'
    sh 'python -m venv vendor/virtualenv'
  end

  desc "Destroy virtualenv."
  task :destroy do
    rm_rf 'vendor/virtualenv'
  end

  desc "Ensure virtualenv is present."
  task :ensure do
    unless File.exists?('vendor/virtualenv')
      Rake::Task['virtualenv:create'].invoke
    end
  end
end

namespace :dependencies do
  namespace :install do
    desc "Install ECS Route53 lambda dependencies."
    task :ecs_route53_registration_lambda => ['virtualenv:ensure'] do
      puts 'Running unit tests for ecs_route53_registration lambda'
      puts

      sh_with_virtualenv(
          'pip install -r lambdas/ecs_route53_registration/requirements.txt')
    end

    desc "Install lambda dependencies."
    task :all => ['dependencies:install:ecs_route53_registration_lambda']
  end
end

namespace :test do
  namespace :unit do
    desc "Unit test ECS Route53 lambda."
    task :ecs_route53_registration_lambda => ['dependencies:install:all'] do
      puts 'Running integration tests'
      puts

      sh_with_virtualenv(
          'python -m unittest discover -s ./lambdas/ecs_route53_registration')
    end

    desc "Unit test lambdas."
    task :all => ['test:unit:ecs_route53_registration_lambda']
  end

  namespace :integration do
    RSpec::Core::RakeTask.new(:all => ['terraform:ensure']) do
      ENV['AWS_REGION'] = 'eu-west-2'
      ENV['TF_PLUGIN_CACHE_DIR'] =
          "#{Paths.project_root_directory}/vendor/terraform/plugins"
    end
  end

  desc "Run all tests"
  task :all => %w(test:unit:all test:integration:all)
end

namespace :deployment do
  namespace :prerequisites do
    RakeTerraform.define_command_tasks(
        configuration_name: 'Preliminary infrastructure',
        argument_names: [:deployment_identifier]
    ) do |t, args|
      deployment_configuration =
          configuration.for(:prerequisites, args)

      t.source_directory = deployment_configuration.source_directory
      t.work_directory = deployment_configuration.work_directory

      t.state_file = deployment_configuration.state_file
      t.vars = deployment_configuration.vars
    end
  end

  namespace :harness do
    RakeTerraform.define_command_tasks(
        configuration_name: 'ECS Route53 registration module',
        argument_names: [:deployment_identifier]
    ) do |t, args|
      deployment_configuration =
          configuration.for(:harness, args)

      t.source_directory = deployment_configuration.source_directory
      t.work_directory = deployment_configuration.work_directory

      t.state_file = deployment_configuration.state_file
      t.vars = deployment_configuration.vars
    end
  end
end

namespace :version do
  task :bump, [:type] do |_, args|
    next_tag = latest_tag.send("#{args.type}!")
    repo.add_tag(next_tag.to_s)
    repo.push('origin', 'master', tags: true)
    puts "Bumped version to #{next_tag}."
  end

  task :release do
    next_tag = latest_tag.release!
    repo.add_tag(next_tag.to_s)
    repo.push('origin', 'master', tags: true)
    puts "Released version #{next_tag}."
  end
end

def sh_with_virtualenv command
  virtualenv_path = File.expand_path('vendor/virtualenv/bin')
  existing_path = ENV['PATH']
  path = "#{virtualenv_path}:#{existing_path}"

  system({'PATH' => path}, command) or exit!(1)
end