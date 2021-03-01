helm repo add signalfx https://dl.signalfx.com/helm-repo
helm repo update
helm install --values signalfx-agent-values.yaml --set clusterName=${CLUSTER_NAME} signalfx-agent signalfx/signalfx-agent