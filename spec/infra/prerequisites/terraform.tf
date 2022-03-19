terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 3.42"
    }
    template = {
      source = "hashicorp/template"
      version = "~> 2.1"
    }
    null = {
      source = "hashicorp/null"
      version = "~> 3.1"
    }
  }
}
