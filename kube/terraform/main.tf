terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "2.73.0"
    }
  }
  backend "azurerm" {

  }
}

provider "azurerm" {
  features {}
}