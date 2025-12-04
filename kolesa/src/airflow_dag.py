from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)


from scraper import run_scraper
from cleaner import run_cleaner
from loader import run_loader

default_args = {
    'owner': 'student_team',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'kolesa_trucks_etl',
    default_args=default_args,
    description='ETL pipeline for Kolesa.kz trucks',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 12, 1),
    catchup=False,
    tags=['scraping', 'etl'],
) as dag:

    t1_scrape = PythonOperator(
        task_id='scrape_data',
        python_callable=run_scraper,
    )

    t2_clean = PythonOperator(
        task_id='clean_data',
        python_callable=run_cleaner,
    )

    t3_load = PythonOperator(
        task_id='load_to_sqlite',
        python_callable=run_loader,
    )

    t1_scrape >> t2_clean >> t3_load