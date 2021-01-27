terraform {
  required_providers {
    signalfx = {
      source  = "splunk-terraform/signalfx"
      version = "6.4.0"
    }
  }
}

variable "auth_token" {
  description = "signalfx auth token"
  type        = string
}

variable "credential_id" {
  description = "VictorOps integration id in Signalfx"
  type        = string
}

variable "routing_key" {
  description = "VictorOps routing key"
  type        = string
}

variable "host_names" {
  description = "Create signalfx alerts for these hosts"
  type        = list(string)
}

variable "memory_used" {
  description = "Memory threshold"
  type        = number
}

provider "signalfx" {
  auth_token = var.auth_token
  api_url    = "https://api.us2.signalfx.com"
}

resource "signalfx_detector" "memory_used" {
  count        = length(var.host_names)
  name         = "${var.host_names[count.index]}: Memory usage"
  program_text = <<-EOF
signal = data('memory.used', filter('host', '${var.host_names[count.index]}')).publish(label='A')
detect(when(signal > ${var.memory_used}, '5m')).publish('High memory for last 5 minutes: ${var.host_names[count.index]}')
    EOF
  rule {
    detect_label  = "High memory for last 5 minutes: ${var.host_names[count.index]}"
    description   = "memory usage exceeds ${var.memory_used} for the last 5 minutes"
    severity      = "Critical"
    notifications = ["VictorOps,${var.credential_id},${var.routing_key}"]
  }
}
