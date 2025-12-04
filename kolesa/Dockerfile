FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app


USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*



RUN pip install "apache-airflow==2.7.3" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.7.3/constraints-3.10.txt"
RUN pip install pandas sqlalchemy playwright==1.40.0


ENV AIRFLOW_HOME=/app/airflow
ENV AIRFLOW__CORE__DAGS_FOLDER=/app/src
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False


COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/entrypoint.sh"]