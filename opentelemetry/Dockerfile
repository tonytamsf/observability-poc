FROM python:3.9-alpine
COPY . /app
WORKDIR /app
ENV FLASK_APP=hello.py
ENV SPLK_TRACE_EXPORTER_URL=http://otelcol:14268/api/traces
ENV SPLK_SERVICE_NAME=flask-app
RUN pip install -r requirements.txt
RUN splk-py-trace-bootstrap
EXPOSE 5000
CMD ["splk-py-trace", "flask", "run", "--host=0.0.0.0"]