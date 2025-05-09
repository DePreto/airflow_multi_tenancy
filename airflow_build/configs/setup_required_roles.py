from airflow.providers.fab.auth_manager.models import Role
from airflow.utils.session import provide_session, SASession

DAGS_PERMISSIONS = {
    ('can_delete', 'DAGs'),
    ('can_edit', 'DAGs'),
    ('can_read', 'DAGs'),
}

TEAM_ROLES = {
  'team_beta',
  'team_beta_read',
}


def create_role(role_name: str, session: SASession) -> Role:
    """
    Create role if not exists.

    Parameters
    ----------
    role_name: str
        role name
    session: SASession
        Session instance

    Returns
    -------
    Role
        Role object
    """
    role = session.query(Role).filter_by(name=role_name).first()
    if role:
        print('role {0} already exist in the db'.format(role))
    else:
        role = Role(name=role_name)
        session.add(role)

    return role


@provide_session
def setup_required_roles(session: SASession = None) -> None:
    """
    Setup required roles.

    Parameters
    ----------
    session: SASession
        Session instance
    """
    with session.begin():
        # create required roles
        for role_name in TEAM_ROLES:
            create_role(role_name, session)
        user_without_dags_role = create_role('User_wo_Dags', session)

        # copy permissions from `User` role with excluding DAGS_PERMISSIONS
        user_without_dags_role.permissions.clear()
        user_role = session.query(Role).filter_by(name='User').first()
        for perm in user_role.permissions:
            if (perm.action.name, perm.resource.name) not in DAGS_PERMISSIONS:
                user_without_dags_role.permissions.append(perm)

    print("roles have been successfully configured")


try:
    setup_required_roles()
except Exception as exc:
    raise RuntimeError(str(exc))
