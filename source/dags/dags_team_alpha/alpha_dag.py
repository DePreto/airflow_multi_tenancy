import datetime as dt

from airflow import DAG
from airflow.operators.empty import EmptyOperator

DAG_ID = 'alpha_dag'

with DAG(
    dag_id=DAG_ID,
    start_date=dt.datetime(2025, 2, 21),
    tags=['test'],
    description="""
        Without any specific tags, 
        dag is located in alpha dir, so it's available only for alpha team.
    """,
    schedule=dt.timedelta(minutes=30),
    catchup=False,
    max_active_runs=1,
):
    empty_task = EmptyOperator(task_id='empty')
