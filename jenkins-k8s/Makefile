# assuming you have started a local minikube instance

install-jenkins-crd:
	kubectl apply -f https://raw.githubusercontent.com/jenkinsci/kubernetes-operator/master/deploy/crds/jenkins_v1alpha2_jenkins_crd.yaml

install-jenkins-operator:
	kubectl apply -f https://raw.githubusercontent.com/jenkinsci/kubernetes-operator/master/deploy/all-in-one-v1alpha2.yaml

deploy-jenkins:
	kubectl apply -f jenkins-instance.yaml

export SFX_REALM=us2
export CLUSTER_NAME= # replace with your minikube cluster name.
export SFX_TOKEN= # replace with signalfx token

deploy-signalfx:
	helm repo add signalfx https://dl.signalfx.com/helm-repo
	helm repo update
	helm install --values signalfx-agent/values.yaml \
		--set signalFxAccessToken=${SFX_TOKEN} \
		--set clusterName=${CLUSTER_NAME} \
		--set signalFxRealm=${SFX_REALM} \
		signalfx-agent signalfx/signalfx-agent

delete-signalfx:
	helm uninstall signalfx-agent
