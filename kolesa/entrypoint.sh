#!/bin/bash
airflow db init

airflow users create \
    --username admin \
    --firstname Student \
    --lastname Project \
    --role Admin \
    --email admin@example.com \
    --password admin || true

airflow scheduler &


exec airflow webserver --port 8080 --host 0.0.0.0