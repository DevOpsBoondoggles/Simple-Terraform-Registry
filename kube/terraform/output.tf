

output "storageaccount" {
  value     = azurerm_storage_account.tfreg-wa-sa.primary_blob_endpoint
  sensitive = false
}


output "container" {
  value     = azurerm_storage_container.tfreg-wa-sac
  sensitive = false
}