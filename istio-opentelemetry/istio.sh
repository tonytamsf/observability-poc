curl -L https://istio.io/downloadIstio | sh -
pushd istio-1.9.0
export PATH=$PWD/bin:$PATH

istioctl install --set profile=demo -y \
    --set meshConfig.enableTracing=true \
    --set meshConfig.defaultConfig.tracing.zipkin.address=\$\(HOST_IP\):9080

kubectl label namespace default istio-injection=enabled
kubectl apply -f samples/bookinfo/platform/kube/bookinfo.yaml

kubectl get services
kubectl get pods

# Optional: Check if the bookinfo app is working by running a curl inside the container
# Caution: This will only work after all the pods are ready
# kubectl exec "$(kubectl get pod -l app=ratings -o jsonpath='{.items[0].metadata.name}')" -c ratings -- curl -s productpage:9080/productpage | grep -o "<title>.*</title>"

kubectl apply -f samples/bookinfo/networking/bookinfo-gateway.yaml

echo "visit once all the pods are ready http://127.0.0.1/productpage"

popd

minikube tunnel