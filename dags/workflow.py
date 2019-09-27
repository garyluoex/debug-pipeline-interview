from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

from tasks.download_data import download_url_data
from tasks.join_stations_and_states import join_stations_and_states

default_args = {
    "owner": "Enigma",
    "depends_on_past": False,
    "start_date": datetime(2019, 1, 1),
    "retries": 0,
}

dag = DAG("debug_pipeline", default_args=default_args, schedule_interval=None)

download_stations_data_task = PythonOperator(
    task_id="download_stations_data",
    python_callable=download_url_data,
    op_kwargs={
        "url": "ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt",
        "output_path": "/root/data/ghcnd-stations.txt",
    },
    dag=dag,
)

download_states_data_task = PythonOperator(
    task_id="download_states_data",
    python_callable=download_url_data,
    op_kwargs={
        "url": "ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-states.txt",
        "output_path": "/root/data/ghcnd-states.txt",
    },
    dag=dag,
)

join_stations_and_states_task = PythonOperator(
    task_id="join_stations_and_states",
    python_callable=join_stations_and_states,
    op_kwargs={
        "stations_path": "ghcnd-stations.txt",
        "states_path": "ghcnd-states.txt",
        "output_path": "/root/data/stations-and-states.csv",
    },
    dag=dag,
)

download_stations_data_task.set_downstream(download_states_data_task)
download_states_data_task.set_downstream(join_stations_and_states_task)
