## Open Telemetry Collector Demo
Flask app sending traces to SignalFX.

Uses https://github.com/signalfx/splunk-otel-python and https://github.com/signalfx/splunk-otel-collector

### Run
Set env vars
```
export SPLUNK_ACCESS_TOKEN=<token> 
export SPLUNK_REALM=<realm>
```
Run the app
```
docker-compose up
```
Hit `localhost:5000` to generate traffic. 

In SignalFx select `Metrics`, search for `jaeger` and select `otelcol_receiver_accepted_spans` to see metrics.