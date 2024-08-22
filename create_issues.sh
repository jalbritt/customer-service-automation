#!/bin/bash

for i in {1..100000}
do
  curl -X 'POST' \
    'http://0.0.0.0:8000/api/v1/issues/' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "title": "string",
    "description": "string",
    "status": "Open"
  }'
done
