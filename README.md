# Airflow Multi-Tenancy Project

A ready-to-use solution for role-based DAG access control in Apache Airflow, featuring automated permission management via DAG tags.

For Airflow 2.0, there are plenty of articles on splitting the DAG processor, workers, and pools — but what about UI separation for different teams?
Here’s how to implement it.


## Prerequisites
- Docker and Docker Compose installed
- Unix-like system (for bash commands)

## Initial Setup
One-time actions required for the first-time project setup.

1. **Clone the repository**:
   ```shell
   git clone git@github.com:DePreto/airflow_multi_tenancy.git && cd airflow_multi_tenancy/
   ```

2. **Use default env params**
   ```shell
   cp ./mock.env ./.env
   ```

3. **Configure Airflow user** (prevents container permission issues, especially with volumes):
   ```shell
   mkdir -p ./source/logs &&
   echo -e "AIRFLOW_UID=$(id -u)" >> ./.env
   ```

## Launching the Project
1. **Build Docker images**:
   ```shell
   docker compose -f ./docker-compose.yaml build
   ```

2. **Start the environment**:
   ```shell
   docker compose -f ./docker-compose.yaml up -d
   ```

## What Happens During Startup?
### `init.sh` Execution (defines presets for quick testing)
- Creates base role `User_wo_Dags` - a parent role with **no** default DAG access permissions (`can_read/edit/delete on DAG Runs`).
- Creates empty team roles:  
  - `team_beta` (full access)  
  - `team_beta_read` (read-only)  
- Creates user `team_beta_user` with roles: `User_wo_Dags`, `team_beta`, and `team_beta_read`.

### Cluster Policies (`airflow_local_settings.py`)
- **Auto-tags DAGs** based on their parent folder name (e.g., DAGs in `dags_team_beta/` get tag `team_beta`).
- Assigns tasks to **team-specific pools** based on folder location.

---

## Next Steps
### For Admins
1. **Log in** as the admin user (`airflow`/`airflow`).
2. **Enable the `system_update_team_permissions` DAG** - it:
   - Reads `team_permissions.yaml` (defines team roles and their permissions).
   - Queries the Airflow metadata database to find DAGs with matching tags (auto-assigned or manual).
   - Grants permissions (e.g., `can_read`, `can_edit`) to roles for DAGs with their tags.

### For Team Users
**Log in as `team_beta_user`** (`team_beta_user`/`team_beta_user`) to see:  
- **`beta_dag`**: Visible because it’s in `dags_team_beta/` (auto-tagged `team_beta` → full access).  
- **`alpha_dag_with_beta_read`**: Visible despite being in `dags_team_alpha/` due to its manual `team_beta_read` tag (read-only access).  

---

## Customization
- Edit `team_permissions.yaml` to add/modify team roles and permissions.
- Manually add tags to DAGs (`tags=["team_beta_read"]`) for cross-team access.


Here's the polished English version for your "Stopping docker-compose" section:

---

## Stopping the Environment

### Graceful Shutdown (Preserves Data)
Use this to retain all Airflow metadata (connections, variables, DAG states):  
```shell
docker compose -f ./docker-compose.yaml -f down
```

### Complete Cleanup (Removes Volumes)
Add `-v` to delete all persistent data (Docker volumes):  
```shell
docker compose -f ./docker-compose.yaml down -v
```
