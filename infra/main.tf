terraform {
  required_version = ">= 1.6"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }

  backend "azurerm" {
    resource_group_name  = "terraform-rg"
    storage_account_name = "mortcalterraform"
    container_name       = "terraform"
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}
