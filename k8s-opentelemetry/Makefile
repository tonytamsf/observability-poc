CLUSTER_NAME=${CLUSTER_NAME:-local}
# SFX_TOKEN=
# SFX_REALM=

install-smartagent: start-cluster
	helm repo add signalfx https://dl.signalfx.com/helm-repo
	helm repo update
	helm install \
	--values kube/signalfx-agent-values.yaml \
	--set signalFxAccessToken=${SFX_TOKEN} \
	--set clusterName=${CLUSTER_NAME} \
	--set signalFxRealm=${SFX_REALM} signalfx-agent signalfx/signalfx-agent

install-otelagent: start-cluster
	envsubst < kube/signalfx-otel.yaml | kubectl apply -f -

install-minikube:
	brew install minikube 2>/dev/null || true

install-redis: start-cluster
	helm repo update
	helm install my-release bitnami/redis

install-helm:
	brew install helm
	helm repo add bitnami https://charts.bitnami.com/bitnami

start-cluster: install-minikube install-helm
	minikube start \
	--memory=4096 \
	--cpus=2 \
	--kubernetes-version=v1.18.10

start-redis: install-redis
	REDIS_PASSWORD=$(kubectl get secret --namespace default my-release-redis -o jsonpath="{.data.redis-password}" | base64 --decode) \
	kubectl create secret generic redis-password --from-literal=password=${REDIS_PASSWORD}

start-app: build-app install-smartagent install-otelagent start-redis
	kubectl apply -f kube/app.yaml
	kubectl expose deployment flask-deployment --type=LoadBalancer --port=5000

build-app: start-cluster
	sh ./build-app.sh

start: start-app

clean:
	minikube stop && minikube delete

