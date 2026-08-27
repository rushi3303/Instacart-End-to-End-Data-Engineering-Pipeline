from agent.gemini_service import GeminiService


def detect_intent(question):
    """
    Uses Gemini to understand the user's question
    and select the most appropriate agent.

    Returns only the agent name so that the
    existing main.py flow remains unchanged.
    """

    gemini = GeminiService()

    prompt = f"""
You are an intelligent router for an
Instacart End-to-End Data Engineering Agentic AI system.

Your job is to understand the user's question semantically
and select the ONE best agent to handle it.

Available agents:

1. data_agent
   - Questions about Instacart data
   - Users/customers
   - Orders
   - Products
   - Departments
   - Aisles
   - Reorders
   - Counts, totals, averages, percentages
   - Data analysis based on PostgreSQL
   - Database queries
   - Data quality or validation questions

2. insight_agent
   - Business analysis
   - Why/how analysis
   - Trends
   - Patterns
   - Comparisons
   - Business insights
   - Questions requiring interpretation of data

3. pipeline_agent
   - ETL pipeline
   - Airflow
   - DAGs
   - Pipeline execution
   - Pipeline status
   - Pipeline failures
   - Tasks
   - Pipeline monitoring

4. ml_agent
   - Customer reorder prediction
   - Product demand prediction
   - Questions about reorder probability
   - Questions about whether a product may be reordered
   - Questions about product demand prediction
   - Machine learning model related to order/customer behavior

5. report_agent
   - Generate a report
   - Create a report
   - Full business/data report
   - Summary report

6. action_agent
   - Recommended actions
   - What should we do?
   - Business recommendations
   - Suggested next actions

7. support_agent
   - Project explanation
   - Architecture
   - Technologies
   - Bronze/Silver/Gold
   - Medallion architecture
   - Data engineering concepts
   - General project-related questions
   - Questions that do not belong to another specialized agent

IMPORTANT RULES:

- Understand the meaning of the question, NOT just keywords.
- Do not depend on exact words such as "customer", "order", "sales", etc.
- A user may ask the same question in many different ways.
- If the question asks for current Instacart data, choose data_agent.
- If the question asks for explanation or business interpretation, choose the appropriate specialized agent.
- Select exactly ONE agent.
- Do not explain your decision.
- Do not return JSON.
- Return ONLY one of these exact values:

data_agent
insight_agent
pipeline_agent
ml_agent
report_agent
action_agent
support_agent

User Question:
{question}
"""

    try:

        response = gemini.generate_response(prompt)

        agent = response.strip().lower()

        allowed_agents = {
            "data_agent",
            "insight_agent",
            "pipeline_agent",
            "ml_agent",
            "report_agent",
            "action_agent",
            "support_agent"
        }

        if agent in allowed_agents:
            return agent

        # Fallback if Gemini returns unexpected output
        return "support_agent"

    except Exception:
        # Safe fallback
        return "support_agent"