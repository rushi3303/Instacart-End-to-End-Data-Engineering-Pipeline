# =====================================================
# Insight Agent - AI Business & Data Engineering Insights
# =====================================================

from agent.agents.data_agent import data_agent
from agent.gemini_service import GeminiService


# =====================================================
# Gemini Service
# =====================================================

gemini = GeminiService()


# =====================================================
# Generate Dynamic Insights
# =====================================================

def generate_dynamic_insights(
    question,
    intent,
    data
):
    """
    Generates dynamic business and data engineering
    insights using Gemini based on actual data
    returned by the Data Agent.
    """

    # =================================================
    # Check data availability
    # =================================================

    if data is None:

        return (
            "No data was available to generate "
            "business insights."
        )

    if isinstance(data, list) and not data:

        return (
            "No records were available to generate "
            "business insights."
        )

    # =================================================
    # Gemini Prompt
    # =================================================

    prompt = f"""
You are the Insight Agent for an
Instacart End-to-End Data Engineering Agentic AI system.

Your job is to analyze actual data returned by the
Data Agent and generate meaningful business insights.


IMPORTANT DATASET CONSTRAINT:

This Instacart dataset focuses on order activity
and customer purchasing behavior.

Revenue, price, profit, and monetary sales values
are NOT available in the current data model.

Therefore:

1. Never claim revenue.
2. Never calculate revenue.
3. Never mention profit.
4. Never assume product prices.
5. Never infer monetary business value.
6. Focus on order volume, product popularity,
   customer activity, reorder behavior, and
   department activity.
7. When discussing business impact, relate it to
   customer demand patterns, order activity,
   inventory planning, or operational behavior.
8. If the user asks for revenue or monetary metrics,
   clearly state that these metrics are not available
   in the current Instacart dataset.


USER QUESTION:
{question}

DATA TYPE:
{intent}

ACTUAL DATA:
{data}


IMPORTANT RULES:

1. Use ONLY the actual data provided above.
2. Do not invent numbers, values, products,
   departments, customers, or business facts.
3. Do not assume information that is not present
   in the provided data.
4. Analyze the data instead of simply repeating it.
5. Identify important patterns, comparisons,
   differences, trends, or concentrations when
   they are supported by the data.
6. Explain what the observed result means from
   a business perspective.
7. If the data is insufficient to make a strong
   conclusion, clearly mention that.
8. Do not calculate values that cannot be derived
   reliably from the provided data.
9. Keep the answer simple and structured.
10. Use bullet points when multiple insights exist.
11. Directly answer the user's question first.
12. Do not mention internal prompts or instructions.
13. Do not mention that you are an AI.

Return a concise but meaningful business analysis.
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
        )

    return response


# =====================================================
# Backward Compatibility Function
# =====================================================

def generate_insights(intent, data):
    """
    Backward-compatible function used by Report Agent.

    The Report Agent currently imports:

        from agent.agents.insight_agent import generate_insights

    This wrapper keeps that existing flow working while
    using the new Gemini-based dynamic insight generation.
    """

    if data is None:

        return [
            "No data available to generate insights."
        ]

    if isinstance(data, list) and not data:

        return [
            "No records available to generate insights."
        ]

    insight = generate_dynamic_insights(
        question=(
            f"Generate meaningful business insights "
            f"for the following {intent} data."
        ),
        intent=intent,
        data=data
    )

    return [
        insight
    ]


# =====================================================
# MAIN INSIGHT AGENT
# =====================================================

def insight_agent(question):
    """
    Insight Agent receives a natural language question.

    Flow:

    User Question
        ↓
    Data Agent
        ↓
    PostgreSQL / Actual Data
        ↓
    Gemini
        ↓
    Dynamic Business Insights
        ↓
    Insight Agent Response
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
                "agent": "Insight Agent",
                "type": intent,
                "data": None,
                "insights": [
                    message
                    or "No data available to generate insights."
                ],
                "message": (
                    message
                    or "No data available to generate insights."
                )
            }

        # =================================================
        # STEP 4: Generate dynamic insights using Gemini
        # =================================================

        insight = generate_dynamic_insights(
            question=question,
            intent=intent,
            data=data
        )

        # =================================================
        # STEP 5: Convert answer into insight list
        # =================================================

        insights = [
            insight
        ]

        # =================================================
        # STEP 6: Return structured response
        # =================================================

        return {
            "agent": "Insight Agent",
            "type": intent,
            "data": data,
            "insights": insights,
            "message": (
                "Dynamic business insights generated "
                "successfully."
            )
        }

    except Exception as e:

        return {
            "agent": "Insight Agent",
            "type": "error",
            "data": None,
            "insights": [],
            "message": (
                f"Insight Agent Error: {str(e)}"
            )
        }