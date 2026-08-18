import os
import re
import json
import base64
import socket
import urllib.request

from sqlalchemy import text
from agent.tools.postgres_tool import engine


# =====================================================
# Airflow DAG File Path
# =====================================================

AIRFLOW_DAG_PATH = os.path.join(
    os.getcwd(),
    "airflow",
    "dags",
    "instacart_etl_dag.py"
)


# =====================================================
# Check if Airflow server is running
# =====================================================

def is_port_open(host="localhost", port=8080, timeout=0.5):

    try:

        with socket.create_connection(
            (host, port),
            timeout=timeout
        ):
            return True

    except Exception:

        return False


# =====================================================
# Get Airflow DAG Information
# =====================================================

def get_airflow_dag_info():

    info = {
        "dag_id": "instacart_etl_pipeline",
        "owner": "Rushikesh",
        "description": "End-to-End Instacart Data Engineering Pipeline",
        "schedule": "Manual Trigger",
        "start_date": "2026-07-10",

        "tasks": [
            {
                "task_id": "load_to_bronze",
                "target": "Bronze Layer"
            },
            {
                "task_id": "bronze_to_silver",
                "target": "Silver Layer"
            },
            {
                "task_id": "silver_to_gold",
                "target": "Gold Layer"
            },
            {
                "task_id": "scd_type1",
                "target": "SCD Type 1"
            },
            {
                "task_id": "scd_type2",
                "target": "SCD Type 2"
            }
        ],

        "flow": (
            "load_to_bronze → "
            "bronze_to_silver → "
            "silver_to_gold → "
            "scd_type1 → "
            "scd_type2"
        )
    }

    # -----------------------------------------------
    # Read actual DAG ID from DAG file
    # -----------------------------------------------

    if os.path.exists(AIRFLOW_DAG_PATH):

        try:

            with open(
                AIRFLOW_DAG_PATH,
                "r",
                encoding="utf-8"
            ) as file:

                content = file.read()

            dag_match = re.search(
                r'dag_id\s*=\s*["\']([^"\']+)["\']',
                content
            )

            if dag_match:

                info["dag_id"] = dag_match.group(1)

        except Exception as error:

            print(
                f"Error reading DAG file: {error}"
            )

    return info


# =====================================================
# Get Latest Airflow DAG Run From REST API
# =====================================================

def get_latest_airflow_run(dag_id):

    if not is_port_open():

        return {
            "server_running": False,
            "run_data": None
        }

    try:

        url = (
            f"http://localhost:8080"
            f"/api/v1/dags/{dag_id}"
            f"/dagRuns?limit=1"
        )

        request = urllib.request.Request(url)

        credentials = base64.b64encode(
            b"airflow:airflow"
        ).decode("utf-8")

        request.add_header(
            "Authorization",
            f"Basic {credentials}"
        )

        with urllib.request.urlopen(
            request,
            timeout=3
        ) as response:

            data = json.loads(
                response.read().decode("utf-8")
            )

            dag_runs = data.get(
                "dag_runs",
                []
            )

            if dag_runs:

                return {
                    "server_running": True,
                    "run_data": dag_runs[0]
                }

            return {
                "server_running": True,
                "run_data": None
            }

    except Exception as error:

        print(
            f"Airflow API error: {error}"
        )

        return {
            "server_running": True,
            "run_data": None
        }


# =====================================================
# Get Latest Audit Records From PostgreSQL
# =====================================================

def get_latest_audit_status():

    try:

        with engine.connect() as connection:

            query = text("""
                SELECT
                    layer_name,
                    table_name,
                    status,
                    end_time,
                    execution_time_seconds,
                    error_message

                FROM audit.audit_log

                ORDER BY audit_id DESC

                LIMIT 10
            """)

            logs = connection.execute(
                query
            ).fetchall()

            return logs

    except Exception as error:

        print(
            f"Database audit error: {error}"
        )

        return []


# =====================================================
# Get Airflow Execution Status
# =====================================================

def get_airflow_execution_status():

    # -----------------------------------------------
    # DAG INFORMATION
    # -----------------------------------------------

    dag_info = get_airflow_dag_info()

    dag_id = dag_info["dag_id"]

    total_tasks = len(
        dag_info["tasks"]
    )

    # -----------------------------------------------
    # AIRFLOW API
    # -----------------------------------------------

    airflow_result = get_latest_airflow_run(
        dag_id
    )

    airflow_server = (
        "RUNNING"
        if airflow_result["server_running"]
        else "OFFLINE"
    )

    airflow_run = airflow_result["run_data"]

    airflow_run_status = None
    airflow_run_time = None

    if airflow_run:

        airflow_run_status = airflow_run.get(
            "state"
        )

        airflow_run_time = (
            airflow_run.get("end_date")
            or airflow_run.get("start_date")
            or airflow_run.get("logical_date")
        )

    # -----------------------------------------------
    # POSTGRESQL AUDIT LOG
    # -----------------------------------------------

    logs = get_latest_audit_status()

    latest_run_time = None

    successful_tasks = 0
    failed_tasks = []
    running_tasks = []

    for row in logs:

        layer_name = row[0]
        table_name = row[1]

        status = str(
            row[2]
        ).lower()

        end_time = row[3]

        if end_time is not None:

            if (
                latest_run_time is None
                or end_time > latest_run_time
            ):

                latest_run_time = end_time

        task_name = (
            f"{layer_name}.{table_name}"
        )

        if status == "success":

            successful_tasks += 1

        elif status in [
            "failed",
            "error"
        ]:

            failed_tasks.append(
                task_name
            )

        elif status in [
            "running",
            "in_progress"
        ]:

            running_tasks.append(
                task_name
            )

    # -----------------------------------------------
    # DETERMINE OVERALL STATUS
    # -----------------------------------------------

    if airflow_run_status:

        overall_status = (
            airflow_run_status.upper()
        )

    elif failed_tasks:

        overall_status = "FAILED"

    elif running_tasks:

        overall_status = "RUNNING"

    elif logs:

        overall_status = "SUCCESS"

    else:

        overall_status = "NO DATA"

    # -----------------------------------------------
    # Prefer Airflow run time if available
    # -----------------------------------------------

    if airflow_run_time:

        latest_run_time = airflow_run_time

    # -----------------------------------------------
    # FINAL LIVE STATUS
    # -----------------------------------------------

    return {
        "dag_id": dag_id,

        "airflow_server": airflow_server,

        "overall_status": overall_status,

        "latest_run_time": latest_run_time,

        "total_tasks": total_tasks,

        "successful_tasks": successful_tasks,

        "failed_tasks": failed_tasks,

        "running_tasks": running_tasks,

        "airflow_run": airflow_run,

        "db_audit": [
            tuple(row)
            for row in logs
        ]
    }