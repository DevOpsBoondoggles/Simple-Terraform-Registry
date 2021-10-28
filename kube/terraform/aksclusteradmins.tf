data "azuread_client_config" "current" {}

data "azuread_users" "users" {
  user_principal_names = var.aksadminusers
}

resource "azuread_group" "aksclusteradmin" {
  display_name     = var.aksadmingroupname
  owners           = [data.azuread_client_config.current.object_id]
  security_enabled = true
  members = data.azuread_users.users.object_ids
}