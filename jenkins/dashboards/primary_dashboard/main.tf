module "jenkins_slx_total_cpu_usage_chart" {
  source = "../../charts/slx_total_cpu_usage_chart"
  service_name = "jenkins"
}

resource "signalfx_dashboard_group" "jenkins_slx_dashboard_group" {
  name        = "${var.jenkins_cluster_name} Cluster Dashboard"
  description = "Dashboards for ${var.jenkins_cluster_name}"
}

resource "signalfx_dashboard" "jenkins_slx_primary_dashboard" {
  name            = "${var.jenkins_cluster_name} SLx Metrics"
  dashboard_group = signalfx_dashboard_group.jenkins_slx_dashboard_group.id
  time_range      = "-1h"

  chart {
    chart_id = module.jenkins_slx_total_cpu_usage_chart.chart_id
    width    = 12
    height   = 1
    row      = 0
    column   = 1
  }
}
