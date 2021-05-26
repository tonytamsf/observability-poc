import flask
import redis
import os
import logging
from opentelemetry import trace

app = flask.Flask(__name__)
app.config["DEBUG"] = True

logging.basicConfig(level=logging.DEBUG)
logging.info(f"Trace exporter url: {os.environ.get('OTEL_EXPORTER_OTLP_ENDPOINT')}")

@app.route('/')
def hello_world():
    key = flask.request.args.get('key', 'foo')
    host = os.getenv('REDIS_HOST', "redis")
    r = redis.Redis(host=host, port=6379, db=0)
    if not r.exists(key):
        r.set(key, "Hello World")
    return r.get(key)