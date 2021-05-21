FROM python:3.9-buster
RUN mkdir /app
WORKDIR /app
ENV FLASK_APP=hello.py
ENV SPLK_TRACE_EXPORTER_URL=http://otelcol:14268/api/traces
RUN pip install Flask
RUN pip install splunk-opentelemetry==0.8.1
RUN pip install redis
RUN splk-py-trace-bootstrap
EXPOSE 5000
CMD ["splk-py-trace", "flask", "run", "--host=0.0.0.0"]
