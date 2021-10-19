variable "name" {
  type    = string
  default = "tfregkubeblob"
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

variable "sourcecontrol_repo_url" {
  default     = "https://github.com/gabrielmccoll/Simple-Terraform-Registry.git"
  type        = string
  description = "This is where the files to deploy the app are kept "
}

variable "sourcecontrol_branch" {
  default     = "main"
  type        = string
  description = "This is the branch of the sourcecontrol_repo_url to use"
}


variable "tags" {
  default = {
    "AppID"        = "tfreg"
    "BusinessUnit" = "myunit"
    "Environment"  = "development"
    "Owner"        = "jonnymarvello"
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


variable "webappskutier" {
  default = "Basic"
  description = "Basic, Free, Standard, Premium"
}

variable "webapskusize" {
  default = "B1"
  description = "F1, B1,B2, S1 and so on "
}
