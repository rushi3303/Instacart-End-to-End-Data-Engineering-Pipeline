# =====================================================
# Report Agent - Complete Data & Business Report
# =====================================================

from agent.agents.data_agent import data_agent
from agent.agents.insight_agent import generate_insights
from agent.agents.action_agent import generate_actions


def create_report(intent, data):
    """
    Creates a structured report using:

    1. Actual data from Data Agent
    2. Insights from Insight Agent
    3. Actions from Action Agent
    """

    insights = generate_insights(intent, data)

    actions = generate_actions(intent, data)

    report = {
        "title": f"{intent.replace('_', ' ').title()} Report",
        "data": data,
        "insights": insights,
        "recommended_actions": actions
    }

    return report


def report_agent(query):
    """
    Report Agent:

    User Question
        ↓
    Data Agent
        ↓
    Actual Data
        ↓
    Insight Agent
        ↓
    Action Agent
        ↓
    Complete Report
    """

    try:

        # Step 1: Get actual data
        data_result = data_agent(query)

        intent = data_result.get(
            "type",
            "unknown"
        )

        data = data_result.get(
            "data"
        )

        # Step 2: Handle unknown request
        if intent == "unknown":

            return {
                "agent": "Report Agent",
                "type": "unknown",
                "data": None,
                "report": None,
                "message": (
                    "Sorry, I could not identify "
                    "the data required for the report."
                )
            }

        # Step 3: Generate complete report
        report = create_report(
            intent,
            data
        )

        # Step 4: Return report
        return {
            "agent": "Report Agent",
            "type": intent,
            "data": data,
            "report": report,
            "message": (
                "Report generated successfully."
            )
        }

    except Exception as e:

        return {
            "agent": "Report Agent",
            "type": "error",
            "data": None,
            "report": None,
            "message": (
                f"Report Agent Error: {str(e)}"
            )
        }