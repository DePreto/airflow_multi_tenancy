import datetime as dt

from airflow import DAG
from airflow.operators.empty import EmptyOperator

DAG_ID = 'alpha_dag_with_beta_read'

with DAG(
    dag_id=DAG_ID,
    start_date=dt.datetime(2025, 2, 21),
    tags=['test', 'team_beta_read'],
    description="""
        `team_beta_read` tag allows read this dag for team beta 
        from alpha dir though
    """,
    schedule=dt.timedelta(minutes=30),
    catchup=False,
    max_active_runs=1,
):
    empty_task = EmptyOperator(task_id='empty')
