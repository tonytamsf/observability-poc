
import logging
from flask import Flask

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def hello_world():
    return 'Hello, World!'
