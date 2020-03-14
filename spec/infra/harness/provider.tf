provider "aws" {
  region = var.region
  version = "~> 2.53"
}

provider "archive" {
  version = "~> 1.3"
}

provider "template" {
  version = "~> 2.1"
}
