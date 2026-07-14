from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "Rushikesh",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="instacart_etl_pipeline",
    default_args=default_args,
    description="End-to-End Instacart Data Engineering Pipeline",
    start_date=datetime(2026, 7, 10),
    schedule=None,          # Manual Trigger
    catchup=False,
    tags=["instacart", "etl", "data-engineering"],
) as dag:

    # ==========================================
    # Bronze Layer
    # ==========================================
    load_to_bronze = BashOperator(
        task_id="load_to_bronze",
        bash_command="""
        cd /opt/airflow/project &&
        python -m scripts.load.load_to_bronze
        """
    )

    # ==========================================
    # Silver Layer
    # ==========================================
    bronze_to_silver = BashOperator(
        task_id="bronze_to_silver",
        bash_command="""
        cd /opt/airflow/project &&
        python -m scripts.transformation.bronze_to_silver
        """
    )

    # ==========================================
    # Gold Layer
    # ==========================================
    silver_to_gold = BashOperator(
        task_id="silver_to_gold",
        bash_command="""
        cd /opt/airflow/project &&
        python -m scripts.transformation.silver_to_gold
        """
    )

    # ==========================================
    # Pipeline Flow
    # ==========================================
    load_to_bronze >> bronze_to_silver >> silver_to_gold