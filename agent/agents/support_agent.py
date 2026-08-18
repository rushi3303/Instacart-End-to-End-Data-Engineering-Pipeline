from agent.rag.rag_engine import search_project_knowledge


def support_agent(query):
    """
    Support Agent handles questions related to:

    - Project architecture
    - Bronze Layer
    - Silver Layer
    - Gold Layer
    - Medallion Architecture
    - Technologies used
    - Data flow
    - General project explanation

    The agent uses RAG to retrieve relevant
    information from the project knowledge base.
    """

    try:

        # Search relevant project knowledge using RAG
        result = search_project_knowledge(query)

        # If relevant information is found
        if result["found"]:

            return {
                "agent": "Support Agent",
                "type": "project_knowledge",
                "data": result["context"],
                "sources": result["sources"]
            }

        # If no information found
        return {
            "agent": "Support Agent",
            "type": "not_found",
            "data": None,
            "sources": [],
            "message": (
                "Sorry, I could not find relevant information "
                "in the project knowledge base."
            )
        }

    except Exception as e:

        return {
            "agent": "Support Agent",
            "type": "error",
            "data": None,
            "sources": [],
            "message": f"Support Agent Error: {str(e)}"
        }