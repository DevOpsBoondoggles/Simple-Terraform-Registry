resource "azurerm_resource_group" "k8s" {
  name = var.name
  location = var.location
  tags = var.tags
}

resource "azurerm_kubernetes_cluster" "k8s" {
    name                = var.name
    location            = azurerm_resource_group.k8s.location
    resource_group_name = azurerm_resource_group.k8s.name
    sku_tier = "Free"
    dns_prefix = var.name
    role_based_access_control {
    enabled = true
      azure_active_directory {
        managed = true
        admin_group_object_ids = [azuread_group.aksclusteradmin.object_id]
      }
    }
    addon_profile {
    aci_connector_linux {
      enabled = false
    }

    azure_policy {
      enabled = false
    }

    http_application_routing {
      enabled = false
    }

    oms_agent {
      enabled = false
    }
    }
    # linux_profile {
    #     admin_username = "ubuntu"

    #     # ssh_key {
    #     #     key_data = file(var.ssh_public_key)
    #     # }
    # }

    default_node_pool {
        name            = "agentpool"
        vm_size         = "Standard_B2s"
        enable_auto_scaling = true
        min_count = 1
        max_count = 2
        max_pods = 30
    }

    identity {
        type = "SystemAssigned"
    }

    # addon_profile {
    #     oms_agent {
    #     enabled                    = true
    #     log_analytics_workspace_id = azurerm_log_analytics_workspace.test.id
    #     }
    # }

    network_profile {
        load_balancer_sku = "Standard"
        network_plugin = "kubenet"
    }
    
    tags = var.tags
    
}

