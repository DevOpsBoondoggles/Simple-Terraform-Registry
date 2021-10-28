variable "name" {
  type    = string
  default = "tfregkubeblob"
}

variable "aksadmingroup" {
  description = "The Object Id of the managementgroup"
  default = ["ae5eddda-e90e-40c8-bb75-e9b05ac73728"]
  type = set(string)
}

variable "aksadmingroupname" {
  description = "The name of the managementgroup"
  default = "akscluseradmintf"
  type = string
}

variable "aksadminusers" {
  description = "The User Principal Name (email address) of the admin users"
  default = ["gabriel@cloudkingdoms.com"]
  type = set(string)
}

variable "location" {
  default = "uksouth"
  type    = string
}

variable "modulebackend" {
  default     = "azureblob"
  type        = string
  description = "This is where terraform modules will be kept, azureblob or local to the webapp "
}



variable "tags" {
  default = {
    "AppID"        = "tfreg"
    "Environment"  = "development"
    "Owner"        = "gabrielmccoll"
  }
}

variable "IPallow" {
  default = [
    "0.0.32.0/20",
    "0.0.16.0/20"
  ]
}

variable "testblobtarget" {
  default     = "v1/modules/namespace/name/provider/1.0.0/local.zip"
  description = "The path of the testblob to check TF is working"
}

variable "testblobsource" {
  default     = "readme.md"
  description = "The file that will be made into fake blob to test module version"
}


