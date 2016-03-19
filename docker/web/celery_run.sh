#!/bin/sh
# wait for redis
sleep 5
celery --beat -A glue worker