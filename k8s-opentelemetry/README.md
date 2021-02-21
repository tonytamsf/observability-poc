## Flask app -> Smart agent -> Otel Collector -> SignalFx Demo

Set env vars
```
export CLUSTER_NAME=<cluster-name>
export SFX_TOKEN=<token> 
export SFX_REALM=<realm>
```
Run the stack with  
```
make start
```
Stop the stack and remove all it's resources with
```
make clean
```

Hit `localhost:5000/set?key=foo&value=bar` to add data to redis.
Hit `localhost:5000/?key=foo` to query data from redis.

Go to `https://app.us2.signalfx.com/#/apm/monitoring` to see apm data.
