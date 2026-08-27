from agent.rag.embedding_service import EmbeddingService
from agent.rag.vector_store import VectorStore


class RAGEngine:
    """
    Retrieves relevant project knowledge from ChromaDB.
    """

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

    def search(self, question, n_results=3):
        """
        Converts the user question into an embedding
        and retrieves the top relevant document chunks.
        """

        # =================================================
        # STEP 1: Convert question into embedding
        # =================================================

        query_embedding = self.embedding_service.create_embedding(
            question
        )

        # =================================================
        # STEP 2: Search relevant chunks in ChromaDB
        # =================================================

        results = self.vector_store.search(
            query_embedding=query_embedding,
            n_results=n_results
        )

        # =================================================
        # STEP 3: Extract documents
        # =================================================

        documents = results.get(
            "documents",
            [[]]
        )[0]

        # =================================================
        # STEP 4: Extract metadata
        # =================================================

        metadatas = results.get(
            "metadatas",
            [[]]
        )[0]

        # =================================================
        # STEP 5: Handle no results
        # =================================================

        if not documents:

            return {
                "found": False,
                "context": "",
                "sources": []
            }

        # =================================================
        # STEP 6: Combine retrieved chunks
        # =================================================

        context_parts = []

        for index, document in enumerate(documents, start=1):

            context_parts.append(
                f"[Retrieved Context {index}]\n{document}"
            )

        context = "\n\n".join(context_parts)

        # =================================================
        # STEP 7: Collect unique sources
        # =================================================

        sources = []

        for metadata in metadatas:

            if metadata and "source" in metadata:

                source = metadata["source"]

                if source not in sources:
                    sources.append(source)

        return {
            "found": True,
            "context": context,
            "sources": sources
        }


def search_project_knowledge(question, n_results=3):
    """
    Search project knowledge using the RAG pipeline.

    This function is used by the Support Agent.
    """

    rag = RAGEngine()

    return rag.search(
        question=question,
        n_results=n_results
    )