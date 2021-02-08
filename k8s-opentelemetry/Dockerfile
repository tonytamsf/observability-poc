FROM python:3.9.1-buster
WORKDIR /app

ENV SPLK_SERVICE_NAME=mit-minikube-flask
ENV REDIS_HOST=my-release-redis-master.default.svc.cluster.local
RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY main.py .
ENV FLASK_APP=main.py

EXPOSE 5000

# CMD ["python", "main.py"]
RUN splk-py-trace-bootstrap
CMD ["splk-py-trace", "flask", "run", "--host=0.0.0.0"] 