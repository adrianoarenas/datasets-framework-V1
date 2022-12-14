from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    dag_id='london-pollution',
    default_args=default_args,
    description='London Pollution dataset DAG',
    schedule_interval="0 10 * * *",
    catchup=False
)

collection = BashOperator(
    task_id='collection-task',
    bash_command='python3 /opt/airflow/dags/src/london-pollution/collection.py',
    dag=dag
)


collection