FROM python:3.9.1-buster
WORKDIR /app

ENV SPLK_SERVICE_NAME=mit-minikube-flask
ENV REDIS_HOST=my-release-redis-master.default.svc.cluster.local
ENV FLASK_APP=main.py

COPY requirements.txt .
COPY main.py .

RUN python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt && \
    splk-py-trace-bootstrap

EXPOSE 5000

# CMD ["python", "main.py"]
CMD ["splk-py-trace", "flask", "run", "--host=0.0.0.0"] 
