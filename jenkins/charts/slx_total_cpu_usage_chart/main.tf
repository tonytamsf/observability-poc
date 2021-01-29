resource "signalfx_time_chart" "slx_total_cpu_usage_chart" {
  name = "Total CPU usage"

  program_text = <<-EOF
        A = data('cpu.usage.total', filter=filter('service', '${var.service_name}')).publish(label='CPU used')
        EOF

  plot_type         = "LineChart"
  show_data_markers = false

  viz_options {
    label = "CPU used"
    color = "blue"
  }
}
