eval $(minikube docker-env) # Use local docker for minikube
docker build -t flask-app:12.0.0 .
kubectl apply -f app.yaml
kubectl expose deployment flask-deployment --type=LoadBalancer --port=5000
minikube tunnel