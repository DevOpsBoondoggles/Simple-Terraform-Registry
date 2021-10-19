# What is this?

This is some terraform that deploys the [Simple Terraform Registry](https://github.com/gabrielmccoll/Simple-Terraform-Registry) at the main branch.
It creates a Webapp and a storage account.
The Webapp has a managed identity and that identity has permission to the storage account. 
To run this, the service principal needs to have permission to the sub, to have blob contributor permissions and to have user access permissions. 

It will fill in the App Settings that set the registry to look at the storage account for the module files. 

