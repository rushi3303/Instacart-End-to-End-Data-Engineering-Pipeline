from agent.tools.airflow_tool import get_airflow_execution_status


# =====================================================
# PIPELINE AGENT
# =====================================================

def pipeline_agent(question):

    try:

        # Get live pipeline information
        result = get_airflow_execution_status()

        return {
            "agent": "Pipeline Agent",

            "type": "pipeline_status",

            "data": result,

            "message": format_pipeline_response(result)

        }

    except Exception as error:

        return {
            "agent": "Pipeline Agent",

            "type": "pipeline_status",

            "data": None,

            "message": (
                f"Unable to retrieve pipeline status: {error}"
            )
        }


# =====================================================
# FORMAT PIPELINE RESPONSE
# =====================================================

def format_pipeline_response(result):

    latest_run = result.get("latest_run_time")

    if latest_run:

        latest_run = latest_run.strftime(
            "%d %B %Y, %I:%M:%S %p"
        )

    else:

        latest_run = "No pipeline run found"


    failed_tasks = result.get(
        "failed_tasks",
        []
    )

    if failed_tasks:

        failed_text = ", ".join(
            failed_tasks
        )

    else:

        failed_text = "None"


    running_tasks = result.get(
        "running_tasks",
        []
    )

    if running_tasks:

        running_text = ", ".join(
            running_tasks
        )

    else:

        running_text = "None"


    response = f"""
⚙️ PIPELINE STATUS

DAG ID: {result.get("dag_id", "Unknown")}

Airflow Server: {result.get("airflow_server", "Unknown")}

Overall Status: {result.get("overall_status", "Unknown")}

Latest Pipeline Run:
{latest_run}

Total Pipeline Tasks:
{result.get("total_tasks", 0)}

Successful Tasks:
{result.get("successful_tasks", 0)}

Failed Tasks:
{failed_text}

Running Tasks:
{running_text}
"""

    return response.strip()