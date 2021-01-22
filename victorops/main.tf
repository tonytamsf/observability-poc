terraform {
  required_providers {
    victorops = {
      source  = "splunk/victorops"
      version = "0.1.1"
    }
  }
}

variable "api_id" {
  type = string
}

variable "api_key" {
  type = string
}

variable "email_address" {
  type = string
}

provider "victorops" {
  api_id  = var.api_id
  api_key = var.api_key
}

# Create a team within victorops
resource "victorops_team" "team" {
  name = "DevOps-Test"
}
# Create a user within the victorops organization
resource "victorops_user" "user1" {
  first_name = "John"
  last_name  = "Doe"
  user_name  = "jdoex1er"
  email      = var.email_address
  is_admin   = "false"
}

# Assign user to a team
resource "victorops_team_membership" "test-membership" {
  team_id   = victorops_team.team.id
  user_name = victorops_user.user1.user_name
}

# Create phone number contact method for a user
resource "victorops_contact" "contact_phone" {
  user_name = victorops_user.user1.user_name
  type      = "phone"
  value     = "+12345678900"
  label     = "test phone"
}

# Create an Escalation Policy for the team
resource "victorops_escalation_policy" "devops_high_severity" {
  name    = "High Severity"
  team_id = victorops_team.team.id
  step {
    timeout = 0
    entries = [
      {
        type     = "user"
        username = "jdoex1er"
      }
    ]
  }
}

# Create a Routing Key that uses the above Escalation Policy
resource "victorops_routing_key" "infrastructure_high_severity" {
  name    = "infrastructure-high-severity"
  targets = [victorops_escalation_policy.devops_high_severity.id]
}
