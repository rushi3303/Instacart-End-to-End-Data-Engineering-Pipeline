from agent.tools.airflow_tool import get_airflow_execution_status


# =====================================================
# PIPELINE AGENT
# =====================================================

def pipeline_agent(question):

    try:

        # Get live pipeline information
        result = get_airflow_execution_status()

        # Generate question-specific answer
        answer = answer_pipeline_question(
            question,
            result
        )

        return {
            "agent": "Pipeline Agent",

            "type": "pipeline_status",

            "data": result,

            "message": answer
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
# QUESTION-SPECIFIC PIPELINE ANSWER
# =====================================================

def answer_pipeline_question(question, result):

    q = question.lower().strip()


    # =================================================
    # DAG ID
    # =================================================

    if (
        "dag id" in q
        or "dag name" in q
    ):

        return (
            f"The DAG ID is "
            f"{result.get('dag_id', 'Unknown')}."
        )


    # =================================================
    # AIRFLOW SERVER STATUS
    # =================================================

    elif (
        "airflow" in q
        and (
            "running" in q
            or "status" in q
            or "online" in q
            or "offline" in q
        )
    ):

        airflow_status = result.get(
            "airflow_server",
            "Unknown"
        )

        if airflow_status == "RUNNING":

            return "Airflow server is currently running."

        elif airflow_status == "OFFLINE":

            return "Airflow server is currently offline."

        else:

            return (
                f"Airflow server status is "
                f"{airflow_status}."
            )


    # =================================================
    # OVERALL PIPELINE STATUS
    # =================================================

    elif (
        "pipeline status" in q
        or "overall status" in q
        or "pipeline health" in q
    ):

        status = result.get(
            "overall_status",
            "Unknown"
        )

        return (
            f"The overall pipeline status is "
            f"{status}."
        )


    # =================================================
    # LATEST PIPELINE RUN
    # =================================================

    elif (
        "latest pipeline run" in q
        or "latest run" in q
        or "last pipeline run" in q
        or "last run" in q
        or "when did the pipeline run" in q
        or "when was the pipeline run" in q
    ):

        latest_run = result.get(
            "latest_run_time"
        )

        if latest_run:

            latest_run = latest_run.strftime(
                "%d %B %Y, %I:%M:%S %p"
            )

            return (
                f"The latest pipeline run was on "
                f"{latest_run}."
            )

        return "No pipeline run information was found."


    # =================================================
    # DAG TASK COUNT
    # =================================================

    elif (
        (
            "how many" in q
            or "number of" in q
            or "count" in q
        )
        and "task" in q
        and (
            "dag" in q
            or "pipeline" in q
            or "total" in q
        )
    ):

        total_tasks = result.get(
            "total_tasks",
            0
        )

        return (
            f"The Instacart Airflow DAG contains "
            f"{total_tasks} tasks."
        )


    # =================================================
    # SUCCESSFUL ETL EXECUTIONS / AUDIT RECORDS
    # =================================================

    elif (
        (
            "successful" in q
            or "succeeded" in q
            or "success" in q
        )
        and (
            "task" in q
            or "etl" in q
            or "execution" in q
            or "audit" in q
        )
    ):

        successful = result.get(
            "successful_tasks",
            0
        )

        return (
            f"{successful} ETL audit records "
            f"have a SUCCESS status."
        )


    # =================================================
    # FAILED ETL EXECUTIONS
    # =================================================

    elif (
        (
            "failed" in q
            or "failure" in q
        )
        and (
            "task" in q
            or "etl" in q
            or "execution" in q
            or "pipeline" in q
        )
        and (
            "which" in q
            or "what" in q
            or "how many" in q
            or "show" in q
            or "list" in q
        )
    ):

        failed_tasks = result.get(
            "failed_tasks",
            []
        )

        if failed_tasks:

            failed_text = ", ".join(
                failed_tasks
            )

            return (
                f"The following ETL operations "
                f"failed: {failed_text}."
            )

        return "No failed ETL operations were found."


    # =================================================
    # RUNNING ETL EXECUTIONS
    # =================================================

    elif (
        (
            "running" in q
            or "in progress" in q
        )
        and (
            "task" in q
            or "etl" in q
            or "execution" in q
            or "operation" in q
        )
    ):

        running_tasks = result.get(
            "running_tasks",
            []
        )

        if running_tasks:

            running_text = ", ".join(
                running_tasks
            )

            return (
                f"The following ETL operations "
                f"are currently running: "
                f"{running_text}."
            )

        return "There are no currently running ETL operations."


    # =================================================
    # WHY DID PIPELINE / ETL FAIL?
    # =================================================

    elif (
        (
            "why" in q
            or "reason" in q
            or "error" in q
        )
        and (
            "fail" in q
            or "failed" in q
            or "failure" in q
            or "pipeline" in q
            or "etl" in q
        )
    ):

        failed_tasks = result.get(
            "failed_tasks",
            []
        )

        audit_records = result.get(
            "db_audit",
            []
        )

        failure_details = []

        for row in audit_records:

            if len(row) >= 6:

                layer_name = row[0]
                table_name = row[1]
                status = str(
                    row[2]
                ).lower()
                error_message = row[5]

                if (
                    status in [
                        "failed",
                        "error"
                    ]
                ):

                    operation = (
                        f"{layer_name}.{table_name}"
                    )

                    if error_message:

                        failure_details.append(
                            f"{operation}: "
                            f"{error_message}"
                        )

                    else:

                        failure_details.append(
                            operation
                        )

        if failure_details:

            return (
                "Pipeline failure details:\n"
                + "\n".join(
                    f"- {detail}"
                    for detail in failure_details
                )
            )

        if failed_tasks:

            failed_text = ", ".join(
                failed_tasks
            )

            return (
                f"The failed ETL operations are: "
                f"{failed_text}. "
                "No detailed error message was found."
            )

        return (
            "No pipeline failure was found "
            "in the available audit records."
        )


    # =================================================
    # DID PIPELINE SUCCEED?
    # =================================================

    elif (
        (
            "did the pipeline succeed" in q
            or "pipeline succeed" in q
            or "pipeline successful" in q
            or "was the pipeline successful" in q
        )
    ):

        status = str(
            result.get(
                "overall_status",
                "Unknown"
            )
        ).upper()

        if status == "SUCCESS":

            return (
                "Yes. The latest pipeline execution "
                "was successful."
            )

        elif status == "FAILED":

            return (
                "No. The latest pipeline execution "
                "failed."
            )

        elif status == "RUNNING":

            return (
                "The pipeline is currently running."
            )

        else:

            return (
                f"The current pipeline status is "
                f"{status}."
            )


    # =================================================
    # COMPLETE PIPELINE STATUS
    # =================================================

    elif (
        "complete pipeline" in q
        or "full pipeline" in q
        or "pipeline summary" in q
        or "complete status" in q
        or "full status" in q
        or "show pipeline status" in q
        or "show me the pipeline status" in q
    ):

        return format_pipeline_response(
            result
        )


    # =================================================
    # DEFAULT PIPELINE RESPONSE
    # =================================================

    else:

        return format_pipeline_response(
            result
        )


# =====================================================
# FORMAT COMPLETE PIPELINE RESPONSE
# =====================================================

def format_pipeline_response(result):

    latest_run = result.get(
        "latest_run_time"
    )

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

Airflow DAG Tasks:
{result.get("total_tasks", 0)}

Successful ETL Executions:
{result.get("successful_tasks", 0)}

Failed ETL Executions:
{failed_text}

Running ETL Executions:
{running_text}
"""

    return response.strip()