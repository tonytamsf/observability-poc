module "jenkins_primary_dashboard" {
  source = "./dashboards/primary_dashboard"
  jenkins_cluster_name = var.jenkins_cluster_name
}

