from agent.router import detect_intent

from agent.agents.support_agent import support_agent
from agent.agents.data_agent import data_agent
from agent.agents.insight_agent import insight_agent
from agent.agents.action_agent import action_agent
from agent.agents.report_agent import report_agent
from agent.agents.ml_agent import ml_agent
from agent.agents.pipeline_agent import pipeline_agent

from agent.tools.chart_tool import recommend_chart


# =====================================================
# BUILD RESPONSE
# =====================================================

def build_response(result, selected_agent):

    """
    Converts responses from all agents into one
    common format for the Streamlit UI.
    """

    agent_name = result.get("agent", "System")
    result_type = result.get("type", "unknown")
    data = result.get("data")

    # =================================================
    # SUPPORT AGENT
    # =================================================

    if selected_agent == "support_agent":

        response_text = (
            result.get("response")
            or result.get("data")
            or result.get("message")
            or "Information not available."
        )

        return {
            "intent": "project_knowledge",

            "reasoning":
                "The Router selected the Support Agent because "
                "the question is related to project knowledge, "
                "architecture, or concepts.",

            "raw_data": None,

            "formatted_text": str(response_text),

            "chart_info":
                recommend_chart("project_knowledge"),

            "insights": [],

            "actions": [],

            "report_data": {
                "full_text": str(response_text)
            },

            "selected_agent": selected_agent,

            "agent_name": agent_name
        }

    # =================================================
    # DATA AGENT
    # =================================================

    elif selected_agent == "data_agent":

        formatted_text = format_data_response(
            result_type,
            data,
            result.get("message")
        )

        return {
            "intent": result_type,

            "reasoning":
                f"The Router selected the Data Agent to handle "
                f"this {result_type.replace('_', ' ')} request.",

            "raw_data": data,

            "formatted_text": formatted_text,

            "chart_info":
                result.get(
                    "chart",
                    recommend_chart(result_type)
                ),

            "insights": [],

            "actions": [],

            "report_data": {
                "full_text": formatted_text
            },

            "selected_agent": selected_agent,

            "agent_name": agent_name
        }

    # =================================================
    # INSIGHT AGENT
    # =================================================

    elif selected_agent == "insight_agent":

        insights = result.get("insights", [])

        formatted_text = "\n\n".join(
            [
                f"• {insight}"
                for insight in insights
            ]
        )

        return {
            "intent": result_type,

            "reasoning":
                "The Router selected the Insight Agent to "
                "analyze the data and generate business insights.",

            "raw_data": data,

            "formatted_text": formatted_text,

            "chart_info":
                recommend_chart(result_type),

            "insights": insights,

            "actions": [],

            "report_data": {
                "full_text": formatted_text
            },

            "selected_agent": selected_agent,

            "agent_name": agent_name
        }

    # =================================================
    # ACTION AGENT
    # =================================================

    elif selected_agent == "action_agent":

        actions = result.get("actions", [])

        formatted_text = "\n\n".join(
            [
                f"• {action}"
                for action in actions
            ]
        )

        return {
            "intent": result_type,

            "reasoning":
                "The Router selected the Action Agent to "
                "generate recommended business actions.",

            "raw_data": data,

            "formatted_text": formatted_text,

            "chart_info":
                recommend_chart(result_type),

            "insights": [],

            "actions": actions,

            "report_data": {
                "full_text": formatted_text
            },

            "selected_agent": selected_agent,

            "agent_name": agent_name
        }

    # =================================================
    # REPORT AGENT
    # =================================================

    elif selected_agent == "report_agent":

        report = result.get("report", {})

        title = report.get(
            "title",
            "Data Engineering Report"
        )

        report_data = report.get("data", [])

        insights = report.get("insights", [])

        actions = report.get(
            "recommended_actions",
            []
        )

        formatted_text = f"📄 {title}\n\n"

        formatted_text += "DATA:\n"

        formatted_text += format_data_response(
            result_type,
            report_data
        )

        formatted_text += "\n\nINSIGHTS:\n"

        if insights:

            formatted_text += "\n".join(
                [
                    f"• {insight}"
                    for insight in insights
                ]
            )

        else:

            formatted_text += "No insights available."

        formatted_text += "\n\nRECOMMENDED ACTIONS:\n"

        if actions:

            formatted_text += "\n".join(
                [
                    f"• {action}"
                    for action in actions
                ]
            )

        else:

            formatted_text += "No actions available."

        return {
            "intent": result_type,

            "reasoning":
                "The Router selected the Report Agent to "
                "generate a complete report with data, insights, "
                "and recommended actions.",

            "raw_data": report_data,

            "formatted_text": formatted_text,

            "chart_info":
                recommend_chart(result_type),

            "insights": insights,

            "actions": actions,

            "report_data": report,

            "selected_agent": selected_agent,

            "agent_name": agent_name
        }

    # =================================================
    # ML AGENT
    # =================================================

    elif selected_agent == "ml_agent":

        formatted_text = format_data_response(
            result_type,
            data,
            result.get("message")
        )

        return {
            "intent": result_type,

            "reasoning":
                f"The Router selected the ML Agent for "
                f"{result_type.replace('_', ' ')}.",

            "raw_data": data,

            "formatted_text": formatted_text,

            "chart_info":
                recommend_chart(result_type),

            "insights": [],

            "actions": [],

            "report_data": {
                "full_text": formatted_text
            },

            "selected_agent": selected_agent,

            "agent_name": agent_name
        }

    # =================================================
    # PIPELINE AGENT
    # =================================================

    elif selected_agent == "pipeline_agent":

       formatted_text = result.get(
           "message",
           "Pipeline status is not available."
        )

       return {
            "intent": result_type,

            "reasoning":
              "The Router selected the Pipeline Agent to "
              "retrieve the latest ETL pipeline status.",

            "raw_data": data,

            "formatted_text": formatted_text,

            "chart_info":None,
               

            "insights": [],

            "actions": [],

            "report_data": {
              "full_text": formatted_text
            },

            "selected_agent": selected_agent,

            "agent_name": agent_name
        }

    # =================================================
    # UNKNOWN RESPONSE
    # =================================================

    message = result.get(
        "message",
        "Sorry, I could not understand your question."
    )

    return {
        "intent": "unknown",

        "reasoning":
            "The Router could not identify a suitable agent.",

        "raw_data": None,

        "formatted_text": message,

        "chart_info":
            recommend_chart("unknown"),

        "insights": [],

        "actions": [],

        "report_data": {
            "full_text": message
        },

        "selected_agent": "unknown",

        "agent_name": "System"
    }


# =====================================================
# FORMAT DATA RESPONSE
# =====================================================

def format_data_response(result_type, data, message=None):

    """
    Converts agent data into readable text.
    """

    if message:
        return message

    if data is None:
        return "No data available."

    # Dictionary response
    if isinstance(data, dict):

        lines = []

        for key, value in data.items():

            clean_key = (
                key.replace("_", " ").title()
            )

            lines.append(
                f"{clean_key}: {value}"
            )

        return "\n".join(lines)

    # List response
    if isinstance(data, list):

        if not data:
            return "No records found."

        lines = []

        for index, row in enumerate(
            data,
            start=1
        ):

            lines.append(
                f"{index}. {row}"
            )

        return "\n".join(lines)

    return str(data)


# =====================================================
# PROCESS QUESTION
# =====================================================

def process_question(question):

    """
    Main entry point for the Multi-Agent
    AI Data Engineering System.

    Flow:

    User Question
          ↓
        Router
          ↓
    --------------------------------
    Support Agent
    Data Agent
    Insight Agent
    Action Agent
    Report Agent
    ML Agent
    pipeline Agent
    --------------------------------
          ↓
    Unified Response
          ↓
    Streamlit UI
    """

    # Detect which agent should handle question
    selected_agent = detect_intent(question)

    # ================================================
    # SUPPORT AGENT
    # ================================================

    if selected_agent == "support_agent":

        result = support_agent(question)

    # ================================================
    # DATA AGENT
    # ================================================

    elif selected_agent == "data_agent":

        result = data_agent(question)

    # ================================================
    # INSIGHT AGENT
    # ================================================

    elif selected_agent == "insight_agent":

        result = insight_agent(question)

    # ================================================
    # ACTION AGENT
    # ================================================

    elif selected_agent == "action_agent":

        result = action_agent(question)

    # ================================================
    # REPORT AGENT
    # ================================================

    elif selected_agent == "report_agent":

        result = report_agent(question)

    # ================================================
    # ML AGENT
    # ================================================

    elif selected_agent == "ml_agent":

        result = ml_agent(question)

    # ================================================
    # PIPELINE AGENT
    # ================================================

    elif selected_agent == "pipeline_agent":

        result = pipeline_agent(question)   
     
    # ================================================
    # UNKNOWN
    # ================================================

    else:

        result = {
            "agent": "System",
            "type": "unknown",
            "message":
                "Sorry, I could not understand your question."
        }

    # Convert all agent responses
    # into one common format

    return build_response(
        result,
        selected_agent
    )


# =====================================================
# MAIN
# =====================================================

def main():

    print("=" * 60)
    print("MULTI-AGENT AI DATA ENGINEERING SYSTEM")
    print("=" * 60)

    question = input(
        "\nAsk your question: "
    )

    response = process_question(question)

    print("\n" + "=" * 60)

    print(
        f"Selected Agent: "
        f"{response['selected_agent']}"
    )

    print(
        f"Agent Name: "
        f"{response['agent_name']}"
    )

    print("\nResponse:")

    print(
        response["formatted_text"]
    )

    print("=" * 60)


# =====================================================
# RUN APPLICATION
# =====================================================

if __name__ == "__main__":
    main()