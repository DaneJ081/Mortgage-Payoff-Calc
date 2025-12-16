terraform {
  required_version = ">= 1.6"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }

    backend "azurerm" {
    resource_group_name  = "tfstate-rg"
    storage_account_name = "mortcaltfstate"
    container_name       = "tfstate"
  }
}

provider "azurerm" {
  features {}
}