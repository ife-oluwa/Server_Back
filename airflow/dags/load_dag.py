from airflow import DAG, utils
from airflow.operators.python_operator import PythonOperator
from ingest import load_data, del_file
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
    'Anaytical_database_data_loading',
    default_args=default_args,
    schedule_interval='* 1 * * *'
) as dag:
    # find_file = FileSensor(task_id="Find_data_csv",
    #                        poke_interval=30, fs_conn_id="incident_file_sensor", filepath=getenv('CSV_LOCATION'),
    #                        on_failure_callback=_failure_callback)
    load_file = PythonOperator(
        task_id="Load_data_csv", python_callable=load_data)
    delete_file = PythonOperator(
        task_id="Delete_data_csv", python_callable=del_file)


# find_file >>
load_file >> delete_file
