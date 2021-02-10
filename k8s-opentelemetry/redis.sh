helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install my-release bitnami/redis
export REDIS_PASSWORD=$(kubectl get secret --namespace default my-release-redis -o jsonpath="{.data.redis-password}" | base64 --decode)
kubectl create secret generic redis-password --from-literal=password=${REDIS_PASSWORD}