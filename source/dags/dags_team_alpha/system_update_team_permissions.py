import datetime as dt
import os

from airflow import DAG
from airflow.decorators import task
from airflow.models import DagModel, DagTag
from airflow.providers.fab.auth_manager.models import (
    Action,
    Permission,
    Resource,
    Role,
)
from airflow.utils.session import provide_session, SASession

from utils.custom_logger import logger
from utils.support_functions import read_yaml_file

DAG_ID = 'system_update_team_permissions'


def get_team_actions() -> dict:
    """
    Get actions by team.

    Returns
    -------
    dict
        team actions
    """
    return read_yaml_file(
        file_address=os.path.join(
            os.environ.get('SOURCE_PATH', os.getcwd()),
            'workdir',
            'utils',
            'team_permissions.yaml',
        ),
    )


@provide_session
def get_dag_ids_by_team(team: str, session: SASession = None) -> set:
    """
    Get set of dag_ids by team.

    Parameters
    ----------
    team: str
        team
    session: SASession
        Session instance

    Returns
    -------
    Set
        dag ids by team
    """
    all_dags_models = session.query(DagModel.dag_id).filter(
        DagModel.tags.any(DagTag.name == team),
    ).all()
    return {dag.dag_id for dag in all_dags_models}


@provide_session
def update_perms(
    team: str,
    dag_ids: set,
    actions: list,
    session: SASession = None,
) -> None:
    """
    Update role permissions.

    Parameters
    ----------
    team: str
        team name
    dag_ids: set
        set of dag_ids
    actions: list
        list of actions
    session: SASession
        Session instance

    Raises
    ------
    ValueError
        Role doesn't exist
    """
    with session.begin():  # delete & update by one transaction
        role = session.query(Role).filter_by(name=team).first()

        if not role:
            raise ValueError("Role doesn't exist")

        role.permissions.clear()  # delete current permissions

        for dag_id in dag_ids:
            for action_name in actions:
                action = session.query(Action).filter_by(
                    name=action_name,
                ).first()
                resource = session.query(Resource).filter_by(
                    name='DAG:{0}'.format(dag_id),
                ).first()
                permission = session.query(Permission).filter_by(
                    action=action,
                    resource=resource,
                ).first()
                role.permissions.append(permission)


@task
def update_team_permission() -> None:
    """Update team permissions."""
    team_actions = get_team_actions()

    for team, actions in team_actions.items():
        dag_ids = get_dag_ids_by_team(team)
        if not dag_ids:
            continue

        update_perms(team, dag_ids, actions)
        logger.info('updated for {0}'.format(team))


with DAG(
    dag_id=DAG_ID,
    start_date=dt.datetime(2025, 2, 21),
    description='Update team permissions',
    tags=['system', 'airflow'],
    schedule=dt.timedelta(minutes=5),
    catchup=False,
    max_active_runs=1,
):
    update_team_permission()
