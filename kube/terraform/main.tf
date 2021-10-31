terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "2.73.0"
    }
    azuread = {
      source = "hashicorp/azuread"
      version = "2.7.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.0.1"
    }

    helm = {
      source = "hashicorp/helm"
      version = "2.3.0"
    }
  }
  # backend "azurerm" {

  # }
}

provider "azurerm" {
  features {}
}