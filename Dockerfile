FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Warsaw

RUN apt-get update && \
        apt-get install -y software-properties-common python3-pip git perl curl make build-essential wget gcc netcat

WORKDIR /app

COPY . .

RUN python3 -m pip install -r requirements.txt --no-cache-dir
CMD ["bash", "run-server.sh"]
