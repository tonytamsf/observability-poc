## Open Telemetry Collector
Flask app sending traces to SignalFX.

Uses https://github.com/signalfx/splunk-otel-python and https://github.com/signalfx/splunk-otel-collector

### Run
Run the app
```
docker build -t flask-app .
docker run --rm -p 5000:5000 flask-app
```
Run the collector
```
docker run --rm -e SPLUNK_ACCESS_TOKEN=<token> -e SPLUNK_BALLAST_SIZE_MIB=683 \
    -e SPLUNK_REALM=<realm> -p 13133:13133 -p 14250:14250 -p 14268:14268 -p 55678-55680:55678-55680 \
    -p 6060:6060 -p 7276:7276 -p 8888:8888 -p 9411:9411 -p 9943:9943 \
    --name otelcol quay.io/signalfx/splunk-otel-collector:0.3.0
```
Now hit `localhost:5000` to generate traffic. 

In SignalFx select `Metrics` and search for `jaeger` and select `otelcol_receiver_accepted_spans` to see metrics.