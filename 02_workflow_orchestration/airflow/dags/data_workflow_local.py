import os

from datetime import datetime

from airflow import DAG

from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from ingest_data import ingest_callable


AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

PG_HOST = os.getenv('PG_HOST')
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_PORT = os.getenv('PG_PORT')
PG_DATABASE = os.getenv('PG_DATABASE')

local_workflow = DAG(
    "LocalIngestionDag",
    schedule_interval="0 6 2 * *",
    start_date=datetime(2025, 4, 1),
    catchup=False # Prevents backfilling
)

URL_PREFIX = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz' 
# URL_TEMPLATE = URL_PREFIX + '/yellow_tripdata_{{ execution_date.strftime(\'%Y-%m\') }}.csv'
OUTPUT_GZ =  AIRFLOW_HOME + '/output_{{ execution_date.strftime("%Y-%m") }}.csv.gz'
OUTPUT_CSV = AIRFLOW_HOME + '/output_{{ execution_date.strftime("%Y-%m") }}.csv'
TABLE_NAME_TEMPLATE = 'yellow_taxi_{{ execution_date.strftime(\'%Y_%m\') }}'



with local_workflow:
    download_task = BashOperator(
        task_id='download',
        bash_command=f'curl -sSL {URL_PREFIX} > {OUTPUT_GZ}'
    )

    unzip_task = BashOperator(
        task_id='unzip',
        bash_command=f'gunzip -f {OUTPUT_GZ}'
    )

    ingest_task = PythonOperator(
        task_id="ingest",
        python_callable=ingest_callable,
        op_kwargs=dict(
            user=PG_USER,
            password=PG_PASSWORD,
            host=PG_HOST,
            port=PG_PORT,
            db=PG_DATABASE,
            table_name=TABLE_NAME_TEMPLATE,
            csv_name=OUTPUT_CSV
        ),
    )

    download_task >> unzip_task >> ingest_task