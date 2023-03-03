from airflow import DAG, utils
from airflow.operators.python_operator import PythonOperator
from ingest import data_ingest
from os import getenv


CSV_LOCATION = getenv("CSV_LOCATION")


default_args = {

    "depends_on_past": False,
    "start_date": utils.dates.days_ago(0),
    'retries': 1,
}


# def _failure_callback(context):
# if isinstance(context['exception'], AirflowSensorTimeout):
#     print(context)
#     print("Sensor timed out")


with DAG(
    'Download_time_series_data',
    default_args=default_args,
    schedule_interval='@daily'
) as dag:
    download_file = PythonOperator(
        task_id="Load_data_csv", python_callable=data_ingest)


download_file
