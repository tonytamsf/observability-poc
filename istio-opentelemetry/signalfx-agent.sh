helm repo add signalfx https://dl.signalfx.com/helm-repo
helm repo update
helm install --values signalfx-agent-values.yaml --set signalFxAccessToken=${SFX_TOKEN} --set clusterName=${CLUSTER_NAME} --set signalFxRealm=${SFX_REALM} signalfx-agent signalfx/signalfx-agent