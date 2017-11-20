require 'rspec/core/rake_task'
require 'securerandom'
require 'git'
require 'semantic'
require 'rake_terraform'

require_relative 'lib/configuration'

configuration = Configuration.new

RakeTerraform.define_installation_tasks(
    path: File.join(Dir.pwd, 'vendor', 'terraform'),
    version: '0.10.8')

task :default => 'test:all'

namespace :virtualenv do
  task :create do
    mkdir_p 'vendor'
    sh 'virtualenv vendor/virtualenv --no-site-packages'
  end

  task :destroy do
    rm_rf 'vendor/virtualenv'
  end

  task :ensure do
    unless File.exists?('vendor/virtualenv')
      Rake::Task['virtualenv:create'].invoke
    end
  end
end

namespace :dependencies do
  namespace :install do
    task :ecs_route53_registration_lambda => ['virtualenv:ensure'] do
      sh_with_virtualenv(
          'pip install -r lambdas/ecs_route53_registration/requirements.txt')
    end

    task :all => ['dependencies:install:ecs_route53_registration_lambda']
  end
end

namespace :test do
  namespace :unit do
    task :ecs_route53_registration_lambda => ['dependencies:install:all'] do
      sh_with_virtualenv(
          'python -m unittest discover -s ./lambdas/ecs_route53_registration')
    end

    task :all => ['test:unit:ecs_route53_registration_lambda']
  end

  namespace :integration do
    RSpec::Core::RakeTask.new(:all => ['terraform:ensure']) do
      ENV['AWS_REGION'] = 'eu-west-2'
    end
  end

  task :all => %w(test:unit:all test:integration:all)
end

namespace :deployment do
  RakeTerraform.define_command_tasks do |t|
    t.argument_names = [:deployment_identifier]

    t.configuration_name = 'ECS Route53 registration module'
    t.source_directory = configuration.source_directory
    t.work_directory = configuration.work_directory

    t.state_file = configuration.state_file

    t.vars = lambda do |args|
      configuration
          .vars_for(args)
          .to_h
    end
  end
end

namespace :release do
  desc 'Increment and push tag'
  task :tag do
    repo = Git.open('.')
    tags = repo.tags
    latest_tag = tags.map { |tag| Semantic::Version.new(tag.name) }.max
    next_tag = latest_tag.increment!(:patch)
    repo.add_tag(next_tag.to_s)
    repo.push('origin', 'master', tags: true)
  end
end

def sh_with_virtualenv command
  virtualenv_path = File.expand_path('vendor/virtualenv/bin')
  existing_path = ENV['PATH']
  path = "#{virtualenv_path}:#{existing_path}"

  system({'PATH' => path}, command) or exit!(1)
end