# Assumption: brew and a hyperdriver (e.g. docker desktop) is already installed
brew install minikube
minikube start --memory=4096 --cpus=2 --kubernetes-version=v1.18.10
