from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

proj_dir = '/opt/airflow/dags/src/london-pollution'
modules_dir = '/opt/airflow/dags/modules'

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
    bash_command=f'python3 {proj_dir}/collection.py',
    dag=dag
)

load = BashOperator(
    task_id='load-task',
    bash_command=f'python3 {proj_dir}/load.py',
    dag=dag
)

db_transformation = BashOperator(
    task_id='transformation-task',
    bash_command=f'python3 {modules_dir}/sqlExecutor.py {proj_dir}/processing_script_1.sql',
    dag=dag
)

collection >> load >> db_transformation