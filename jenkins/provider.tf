terraform {
  required_providers {
    signalfx = {
      source = "splunk-terraform/signalfx"
      version = "6.4.0"
    }
  }
}

provider "signalfx" {
  auth_token = var.signalfx_auth_token
  api_url = "https://api.us2.signalfx.com"
}

