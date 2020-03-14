Terraform AWS ECS Route53 Registration
======================================

[![CircleCI](https://circleci.com/gh/infrablocks/terraform-aws-ecs-route53-registration.svg?style=svg)](https://circleci.com/gh/infrablocks/terraform-aws-ecs-route53-registration)

A Terraform module for registering containers in an ECS service in Route53.

The ECS service requires:
* An existing VPC
* An ECS cluster
* An ECS service
* Route53 zone(s)

The ECS Route53 registration consists of:
* A lambda that listens to ECS events and registers containers into Route53

![Diagram of infrastructure managed by this module](/docs/architecture.png?raw=true)

Usage
-----

To use the module, include something like the following in your terraform
configuration:

```hcl-terraform
module "ecs_route53_registration" {
  source = "git@github.com:infrablocks/terraform-aws-ecs-route53-registration.git"
}
```

As mentioned above, the registration lambda works with an existing base network 
and ECS cluster for an existing ECS service. Whilst these can be created using 
any mechanism you like, the following modules may be of use: 
* [AWS Base Networking](https://github.com/infrablocks/terraform-aws-base-networking)
* [AWS ECS Cluster](https://github.com/infrablocks/terraform-aws-ecs-cluster)
* [AWS ECS Service](https://github.com/infrablocks/terraform-aws-ecs-service)


### Inputs

| Name                      | Description                      | Default            | Required |
|---------------------------|----------------------------------|:------------------:|:--------:|


### Outputs

| Name                      | Description                                                          |
|---------------------------|----------------------------------------------------------------------|


Development
-----------

### Machine Requirements

In order for the build to run correctly, a few tools will need to be installed 
on your development machine:

* Ruby (2.3.1)
* Bundler
* git
* git-crypt
* gnupg
* direnv

#### Mac OS X Setup

Installing the required tools is best managed by [homebrew](http://brew.sh).

To install homebrew:

```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Then, to install the required tools:

```
# ruby
brew install rbenv
brew install ruby-build
echo 'eval "$(rbenv init - bash)"' >> ~/.bash_profile
echo 'eval "$(rbenv init - zsh)"' >> ~/.zshrc
eval "$(rbenv init -)"
rbenv install 2.3.1
rbenv rehash
rbenv local 2.3.1
gem install bundler

# git, git-crypt, gnupg
brew install git
brew install git-crypt
brew install gnupg

# direnv
brew install direnv
echo "$(direnv hook bash)" >> ~/.bash_profile
echo "$(direnv hook zsh)" >> ~/.zshrc
eval "$(direnv hook $SHELL)"

direnv allow <repository-directory>
```

### Running the build

To provision module infrastructure, run tests and then destroy that 
infrastructure, execute:

```bash
./go
```

To provision the module test contents:

```bash
./go provision:aws[<deployment_identifier>]
```

To destroy the module test contents:

```bash
./go destroy:aws[<deployment_identifier>]
```

### Common Tasks

#### Generating an SSH key pair

To generate an SSH key pair:

```
ssh-keygen -t rsa -b 4096 -C integration-test@example.com -N '' -f config/secrets/keys/bastion/ssh
```

#### Generating a self-signed certificate

To generate a self signed certificate:
```
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
```

To decrypt the resulting key:

```
openssl rsa -in key.pem -out ssl.key
```

#### Managing CircleCI keys

To encrypt a GPG key for use by CircleCI:

```bash
openssl aes-256-cbc \
  -e \
  -md sha1 \
  -in ./config/secrets/ci/gpg.private \
  -out ./.circleci/gpg.private.enc \
  -k "<passphrase>"
```

To check decryption is working correctly:

```bash
openssl aes-256-cbc \
  -d \
  -md sha1 \
  -in ./.circleci/gpg.private.enc \
  -k "<passphrase>"
```

Contributing
------------

Bug reports and pull requests are welcome on GitHub at 
https://github.com/infrablocks/terraform-aws-ecs-route53-registration. 
This project is intended to be a safe, welcoming space for collaboration, and 
contributors are expected to adhere to 
the [Contributor Covenant](http://contributor-covenant.org) code of conduct.


License
-------

The library is available as open source under the terms of the 
[MIT License](http://opensource.org/licenses/MIT).
