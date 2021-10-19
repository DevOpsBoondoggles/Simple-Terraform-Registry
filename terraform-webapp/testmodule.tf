#create a test blob structure so can see if the blob feedback is working
#go to azurerm_app_service.tfreg-wa-as.default_site_hostname/v1/modules/namespace/name/provider/versions
#you should get something that looks like {"modules": [{"versions": [{"version": "1.0.0"}]}]} back

resource "azurerm_storage_blob" "tfreg-wa-sab" {
  name                   = var.testblobtarget
  type                   = "Block"
  storage_account_name   = azurerm_storage_account.tfreg-wa-sa.name
  storage_container_name = azurerm_storage_container.tfreg-wa-sac.name
  source                 = var.testblobsource
}


