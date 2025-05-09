ARG airflow_version='2.9.3'
ARG python_version='3.12'

FROM apache/airflow:${airflow_version}-python${python_version}

USER airflow
WORKDIR /opt/airflow

RUN pip install apache-airflow==${AIRFLOW_VERSION} apache-airflow[statsd]==${AIRFLOW_VERSION}

ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow/workdir"