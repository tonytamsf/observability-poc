import flask
import os
import logging
from opentelemetry import trace

app = flask.Flask(__name__)
app.config["DEBUG"] = True

logging.basicConfig(level=logging.DEBUG)
logging.info(f"Trace exporter url: {os.environ.get('OTEL_EXPORTER_OTLP_ENDPOINT')}")

@app.route('/')
def hello_world():
    return 'Hello World!'
