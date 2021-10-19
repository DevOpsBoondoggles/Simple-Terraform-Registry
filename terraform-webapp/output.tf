output "appservice" {
  value = [
    azurerm_app_service.tfreg-wa-as.default_site_hostname,
    azurerm_app_service.tfreg-wa-as.tags
  ]
}

output "storageaccount" {
  value     = azurerm_storage_account.tfreg-wa-sa.primary_blob_endpoint
  sensitive = false
}


output "container" {
  value     = azurerm_storage_container.tfreg-wa-sac
  sensitive = false
}