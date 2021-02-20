import flask
import redis
import os
import logging

app = flask.Flask(__name__)
app.config["DEBUG"] = True

logging.basicConfig(level=logging.DEBUG)

logging.info(f"Trace exporter url: {os.environ.get('SPLK_TRACE_EXPORTER_URL')}")

@app.route('/', methods=['GET'])
def getValue():
    key = flask.request.args.get('key', 'foo')
    host = os.getenv('REDIS_HOST', "localhost")
    r = redis.Redis(host=host, port=6379, db=0, password=open("/secrets/redis/password").read())
    v = r.get(key)
    return v

@app.route('/set', methods=['GET'])
def setValue():
    key = flask.request.args.get('key')
    value = flask.request.args.get('value')
    host = os.getenv('REDIS_HOST', "localhost")
    r = redis.Redis(host=host, port=6379, db=0, password=open("/secrets/redis/password").read())
    r.set(key, value)
    return value

if __name__ == "__main__":
    app.run()