from datetime import timedelta, datetime

from airflow import DAG
from airflow.models.baseoperator import chain
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
    'start_date': datetime(2021, 10, 1),
    'schedule_interval': "0 0 * * *",
}

with DAG(dag_id="spark_doge_dag", default_args=default_args, max_active_runs=1) as dag:
    submit_application = SparkKubernetesOperator(
        task_id="submit_spark_doge",
        application_file="spark-doge.yaml",
        namespace="spark",
        kubernetes_conn_id='kubernetes_default',
        api_group='sparkoperator.k8s.io',
        api_version='v1beta2',
        do_xcom_push=True,
    )

    check_application = SparkKubernetesSensor(
        task_id="check_spark_doge",
        application_name="{{ task_instance.xcom_pull(task_ids='submit_spark_doge')['metadata']['name'] }}",
        attach_log=True,
        namespace="spark",
        kubernetes_conn_id="kubernetes_default",
        api_group='sparkoperator.k8s.io',
        api_version='v1beta2',
        mode="reschedule",
        poke_interval=int(timedelta(seconds=30).total_seconds()),
    )

    chain(
        submit_application,
        check_application,
    )
