import datetime
import sys

from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryGetDataOperator
from airflow.operators.python_operator import PythonOperator


def print_data(**kwargs):
    data = kwargs['ti'].xcom_pull(task_ids='get_data_from_bigquery')
    print(data)


sql_query = r'SELECT * FROM `international-football.international_football_dataset.penalty_shootout_vw`'

with DAG(
    dag_id='query_dag',
    start_date=datetime.datetime(2022, 1, 1),
    catchup=False
) as dag:

    query_view = BigQueryExecuteQueryOperator(
        task_id="query_view",
        sql=sql_query,
        destination_dataset_table=f"international_football_dataset.penalty_shootout_test",
        write_disposition="WRITE_TRUNCATE",
        gcp_conn_id="google_cloud_default",
        use_legacy_sql=False,

    )

    get_data = BigQueryGetDataOperator(
        task_id="get_data",
        dataset_id='international_football_dataset',
        table_id='penalty_shootout_test',
    )

    send_data = PythonOperator(
        task_id='send_data',
        python_callable=print_data,
        provide_context=True,
    )

    query_view >> get_data >> send_data
