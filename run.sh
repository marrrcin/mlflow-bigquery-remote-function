#!/bin/bash
set -e
exec uvicorn bq_api:app --proxy-headers --host 0.0.0.0 --port $PORT
