terraform {
  required_providers {
    aws  = {
        source = "hashicorp/aws"
        version = "5.40.0"
    }
  }
}

provider "aws" {
  profile =  var.profile
  assume_role {
    role_arn = var.assume_role
    session_name = "terraform-session"
  }
}