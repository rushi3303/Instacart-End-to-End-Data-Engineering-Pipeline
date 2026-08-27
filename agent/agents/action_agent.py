# =====================================================
# Action Agent - AI Recommended Actions
# =====================================================

from agent.agents.data_agent import data_agent
from agent.gemini_service import GeminiService


# =====================================================
# Gemini Service
# =====================================================

gemini = GeminiService()


# =====================================================
# Generate Dynamic Actions
# =====================================================

def generate_dynamic_actions(
    question,
    intent,
    data
):
    """
    Generates recommended business and
    data engineering actions using Gemini.

    Actions are generated only from the
    actual data returned by the Data Agent.
    """

    # =================================================
    # Check data availability
    # =================================================

    if data is None:

        return (
            "No data was available to "
            "generate recommended actions."
        )

    if isinstance(data, list) and not data:

        return (
            "No records were available to "
            "generate recommended actions."
        )

    # =================================================
    # Gemini Prompt
    # =================================================

    prompt = f"""
You are the Action Agent for an
Instacart End-to-End Data Engineering Agentic AI system.

Your job is to analyze the actual data returned by
the Data Agent and recommend practical next actions.

USER QUESTION:
{question}

DATA TYPE:
{intent}

ACTUAL DATA:
{data}

IMPORTANT DATASET CONTEXT:

This Instacart dataset primarily represents
orders, products, customers, departments,
aisles, reorders, and customer ordering behavior.

Revenue, profit, product price, monetary value,
and total sales amount are NOT available
in the current data model.

IMPORTANT RULES:

1. Use ONLY the actual data provided above.

2. Do not invent numbers, values, products,
   departments, customers, revenue, profit,
   prices, or business facts.

3. Do not recommend actions based on revenue,
   profit, pricing, or monetary value because
   those fields are not available.

4. Recommendations must be supported by
   order behavior, product demand, customer
   activity, reorders, departments, data quality,
   or pipeline information.

5. If the data is insufficient for a strong
   recommendation, clearly mention that.

6. Do not assume information that is not present
   in the provided data.

7. Recommend practical and realistic actions.

8. Prefer 3 to 5 concise recommendations.

9. Directly relate recommendations to
   the user's question.

10. Do not mention internal prompts or instructions.

11. Do not mention that you are an AI.

12. Keep the response simple and structured.

13. Use bullet points.

Return only the recommended actions and
a short explanation of why each action
is useful.
"""

    # =================================================
    # Generate Gemini Response
    # =================================================

    response = gemini.generate_response(prompt)

    # =================================================
    # Handle Gemini Error / Quota
    # =================================================

    if (
        not response
        or response.startswith("Gemini API Error:")
    ):

        return (
            "Gemini is temporarily unavailable. "
            "The Data Agent successfully retrieved "
            "the following data:\n\n"
            + str(data)
            + "\n\n"
            "Recommended actions can be generated "
            "when the Gemini service is available."
        )

    return response


# =====================================================
# Backward Compatibility Function
# =====================================================

def generate_actions(intent, data):
    """
    Backward-compatible function used by Report Agent.

    The Report Agent imports:

        from agent.agents.action_agent import generate_actions

    This wrapper keeps the existing Report Agent flow
    working with the new Gemini-based Action Agent.
    """

    if data is None:

        return [
            "No data available to recommend actions."
        ]

    if isinstance(data, list) and not data:

        return [
            "No records available to recommend actions."
        ]

    action = generate_dynamic_actions(
        question=(
            f"Recommend practical actions "
            f"based on the following {intent} data."
        ),
        intent=intent,
        data=data
    )

    return [
        action
    ]


# =====================================================
# MAIN ACTION AGENT
# =====================================================

def action_agent(question):
    """
    Action Agent receives a natural language question.

    Flow:

    User Question
        ↓
    Data Agent
        ↓
    PostgreSQL / Actual Data
        ↓
    Gemini
        ↓
    Recommended Actions
        ↓
    Action Agent Response
    """

    try:

        # =================================================
        # STEP 1: Get actual data from Data Agent
        # =================================================

        data_result = data_agent(question)

        # =================================================
        # STEP 2: Extract result information
        # =================================================

        intent = data_result.get(
            "type",
            "unknown"
        )

        data = data_result.get(
            "data"
        )

        message = data_result.get(
            "message"
        )

        # =================================================
        # STEP 3: Handle unavailable data
        # =================================================

        if data is None:

            return {
                "agent": "Action Agent",
                "type": intent,
                "data": None,
                "actions": [
                    message
                    or
                    "No data available to recommend actions."
                ],
                "message": (
                    message
                    or
                    "No data available to recommend actions."
                )
            }

        # =================================================
        # STEP 4: Generate dynamic actions
        # =================================================

        actions = generate_dynamic_actions(
            question=question,
            intent=intent,
            data=data
        )

        # =================================================
        # STEP 5: Return structured response
        # =================================================

        return {
            "agent": "Action Agent",
            "type": intent,
            "data": data,
            "actions": [
                actions
            ],
            "message": (
                "Recommended actions generated "
                "successfully."
            )
        }

    except Exception as e:

        return {
            "agent": "Action Agent",
            "type": "error",
            "data": None,
            "actions": [],
            "message": (
                f"Action Agent Error: {str(e)}"
            )
        }