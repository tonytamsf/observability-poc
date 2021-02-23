## Book info app -> Istio (Envoy) -> Smart agent -> Otel Collector -> SignalFx Demo

Set env vars
```
export SFX_TOKEN=<token> 
export SFX_REALM=<realm>
export CLUSTER_NAME=<cluster-name>
```
Install minikube
```
./minikube.sh
```
Install signalfx agent
```
./signalfx-agent.sh
```
Install signalfx otel collector
```
./signalfx-otel.sh
```
Install and run istio and bookinfo app
```
./istio.sh
```

Hit `http://127.0.0.1/productpage` to visit book info application after all the pods are ready

Go to `https://app.us2.signalfx.com/#/apm/monitoring` to see apm data (may take a couple of minutes to for traces to show up)


What works out of the box with this setup?

-  Infrastructure metrics (e.g. cpu, memory, network i/o) for container, pod and node
- Service instrumentation across all services running with an envoy Sidecar.
- When a service calls another service, the request headers from the current request are passed on in the new request
    - https://github.com/openzipkin/b3-propagation
    - This works out of the box in bookinfo application in istio as the implementation passes around the headers.
    - When doing this for our applications, we need to write http request handlers.
    - Note that when using the Otel SDK in the application approach, we don't need to do this.


What doesn't work with this setup?

- Any inter/intra service communication which doesn't happen through envoy sidecar isn't reported.
- If the service doesn't pass existing tracing headers whlie making calls to other services, the new request will be under a new trace (instead of a new span in existing trace)


What value is added by otel in this setup?

Otel does a better job at memory management, batching, compression etc, thus improving the stabiltity of the system.
