#!/bin/bash

python ./configs/setup_required_roles.py || exit 1;

airflow users create \
  --username 'team_beta_user' \
  --password 'team_beta_user' \
  --firstname 'test' \
  --lastname 'test' \
  --role User_wo_Dags \
  --email 'test@example.org';

airflow users add-role \
  --username team_beta_user \
  --role team_beta;

airflow users add-role \
  --username team_beta_user \
  --role team_beta_read;
