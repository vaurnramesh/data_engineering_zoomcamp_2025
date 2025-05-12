import os
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator # type: ignore
from airflow.operators.python import PythonOperator # type: ignore
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator, BigQueryCreateEmptyDatasetOperator # type: ignore
from airflow.providers.google.cloud.hooks.gcs import GCSHook # type: ignore
import requests # type: ignore
import gzip
import shutil
import pyarrow # type: ignore
import pyarrow.csv # type: ignore
import pyarrow.parquet # type: ignore

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET_GREEN")
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", 'trips_data_all')
CONN= os.environ.get("AIRFLOW_CONN_GOOGLE_CLOUD_DEFAULT")