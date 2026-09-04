terraform {
  required_version = ">= 1.11"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = ">= 4.0"
    }
  }

  backend "s3" {
    bucket       = "mortcal-tfstate-056287801929"
    region       = "us-east-1"
    use_lockfile = true
    encrypt      = true
    # key is passed at init time: -backend-config="key=mortcal/<env>/terraform.tfstate"
  }
}

provider "aws" {
  region = var.region
}

# Reads the token from the CLOUDFLARE_API_TOKEN env var - never set inline here.
provider "cloudflare" {}
