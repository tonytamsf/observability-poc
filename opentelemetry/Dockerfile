FROM python:3.9-buster
RUN mkdir /app
WORKDIR /app
ENV FLASK_APP=hello.py
RUN pip install Flask
RUN pip install splunk-opentelemetry[all]==0.14.0
RUN pip install markupsafe==2.0.1
RUN pip install redis
RUN splk-py-trace-bootstrap
EXPOSE 6999
CMD ["splk-py-trace", "flask", "run", "--host=0.0.0.0"]
