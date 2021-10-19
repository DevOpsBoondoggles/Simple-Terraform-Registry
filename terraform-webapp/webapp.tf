resource "azurerm_resource_group" "tfreg-wa-rg" {
  name     = var.name
  location = var.location
  tags     = var.tags
}

resource "azurerm_app_service_plan" "tfreg-wa-asp" {
  name                = "${var.name}-asp"
  location            = azurerm_resource_group.tfreg-wa-rg.location
  resource_group_name = azurerm_resource_group.tfreg-wa-rg.name
  kind                = "Linux"
  reserved            = true #this doesn't seem to mean anything. It just required for a linux plan
  sku {
    tier = var.webappskutier
    size = var.webapskusize
  }
}

resource "azurerm_app_service" "tfreg-wa-as" {
  name                = "${var.name}-asp"
  resource_group_name = azurerm_resource_group.tfreg-wa-rg.name
  location            = azurerm_resource_group.tfreg-wa-rg.location
  app_service_plan_id = azurerm_app_service_plan.tfreg-wa-asp.id
  https_only = true


  site_config {
    linux_fx_version          = "PYTHON|3.8"
    use_32_bit_worker_process = true #this needs to be 32 bit for free tier
    dynamic "ip_restriction" {
      for_each = var.IPallow
      content {
        ip_address = ip_restriction.value
      }
    }
    scm_use_main_ip_restriction = true
  }
    lifecycle {
    ignore_changes = [
      # Ignore changes to tags, e.g. because a management agent
      # updates these based on some ruleset managed elsewhere.
      tags,
      source_control
    ]
    }
  source_control { #this section might need blocked out until first successful deployment. seems to error out
    branch             = var.sourcecontrol_branch
    repo_url           = var.sourcecontrol_repo_url
    manual_integration = true
    
  }

  identity {
    type = "SystemAssigned"
  }

  app_settings = { #this all needs added. see the Simple Terraform Registry at github for explanation
    "MODULEBACKEND"     = var.modulebackend
    "AZBLOBACCOUNTNAME" = azurerm_storage_account.tfreg-wa-sa.name
    "AZBLOBSTORAGEHOST" = azurerm_storage_account.tfreg-wa-sa.primary_blob_endpoint
    "AZCONTAINER"       = azurerm_storage_container.tfreg-wa-sac.name
  }
  tags = var.tags
}