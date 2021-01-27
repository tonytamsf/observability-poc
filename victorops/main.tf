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

variable "first_name" {
  type = string
}

variable "last_name" {
  type = string
}

variable "team_name" {
  type = string
}

variable "user_name" {
  type = string
}

provider "victorops" {
  api_id  = var.api_id
  api_key = var.api_key
}

# Create a team within victorops
resource "victorops_team" "team" {
  name = var.team_name
}

# Create a user within the victorops organization
resource "victorops_user" "user1" {
  first_name = var.first_name
  last_name  = var.last_name
  user_name  = var.user_name
  email      = var.email_address
  is_admin   = "false"
}

# Assign user to a team
resource "victorops_team_membership" "test-membership" {
  team_id   = victorops_team.team.id
  user_name = victorops_user.user1.user_name
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
        username = var.user_name
      }
    ]
  }
}

# Create a Routing Key that uses the above Escalation Policy
resource "victorops_routing_key" "infrastructure_high_severity" {
  name    = "infrastructure-high-severity"
  targets = [victorops_escalation_policy.devops_high_severity.id]
}
