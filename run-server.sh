#!/bin/bash

echo "Waiting for Tika to launch on $TIKA_PORT..."

while ! nc -z $TIKA_HOST $TIKA_PORT; do   
  sleep 1
done

echo "Tika launched"


echo "Waiting for ElasticSearch to launch on $ELASTICSEARCH_PORT..."

while ! nc -z $ELASTICSEARCH_HOST $ELASTICSEARCH_PORT; do   
  sleep 1
done

echo "ElasticSearch launched"


echo "Launching the server"
uvicorn app:app --host 0.0.0.0 --port 9876
