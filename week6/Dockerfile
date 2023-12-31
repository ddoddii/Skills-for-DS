FROM python:3.9-slim

LABEL maintainer="1223cindy@gmail.com"

ENV PYTHONUNBUFFERED = 1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY DockerModel.py DockerModel.py
COPY models/ models/

EXPOSE 5000 9000

ENV MODEL_NAME DockerModel
ENV SERVICE_TYPE MODEL

RUN chown -R 8888 /app

CMD exec seldon-core-microservice $MODEL_NAME --service-type $SERVICE_TYPE