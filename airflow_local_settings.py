from pathlib import Path

from airflow.exceptions import AirflowClusterPolicyViolation
from airflow.models import DAG, BaseOperator


def _dag_policy_add_team_tag(dag: DAG) -> list:
    """
    Add team tag to dag by dag parent folder.

    Parameters
    ----------
    dag: DAG
        dag model

    Returns
    -------
    List
        list of errors
    """
    errors = []

    dag_parent_folder = Path(dag.fileloc).parent.name

    if dag_parent_folder == 'dags_team_beta':
        dag.tags.append('team_beta')
    elif dag_parent_folder == 'dags_team_alpha':
        dag.tags.append('team_alpha')
    else:
        errors.append(
            'Unknown dag parent folder {0}'.format(dag_parent_folder),
        )
    return errors


def dag_policy(dag: DAG) -> None:
    """
    Allow altering or checking DAGs after they are loaded in the DagBag.

    Parameters
    ----------
    dag: DAG
        dag model

    Raises
    ------
    AirflowClusterPolicyViolation
        altering or checking errors
    """
    errors = []

    errors.extend(_dag_policy_add_team_tag(dag))

    if errors:
        raise AirflowClusterPolicyViolation('Errors: {0}'.format(errors))


def task_policy(task: BaseOperator) -> None:
    """
    Allow altering or checking tasks after they are loaded in the DagBag.

    Parameters
    ----------
    task: BaseOperator
        task model
    """
    dag_parent_folder = Path(task.dag.fileloc).parent.name

    if dag_parent_folder == 'dags_team_bi':
        task.pool = 'team_bi_pool'
