import datetime
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryGetDataOperator,
)

with DAG(
    dag_id='example_bq_operator',
    start_date=datetime.datetime(2022, 1, 1),
    catchup=False
) as dag:

    # get_dataset_tables = BigQueryGetDatasetTablesOperator(
    #     task_id="get_dataset_tables", dataset_id='international_football_dataset', gcp_conn_id='google_cloud_default'
    # )

    get_data = BigQueryGetDataOperator(
    task_id="get_data",
    dataset_id='international_football_dataset',
    table_id='penalty_shootout',
    max_results=10,
    selected_fields="date,home_team,away_team,winner",
    location='us-east1',
    )
    get_data