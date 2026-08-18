from agent.rag.embedding_service import EmbeddingService
from agent.rag.vector_store import VectorStore


class RAGEngine:
    """
    Retrieves relevant project knowledge from ChromaDB.
    """

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

    def search(self, question, n_results=1):
        """
        Converts the user question into an embedding
        and retrieves the top relevant document chunks.
        """

        # Step 1: Convert user question into an embedding
        query_embedding = self.embedding_service.create_embedding(
            question
        )

        # Step 2: Search top relevant chunks in ChromaDB
        results = self.vector_store.search(
            query_embedding=query_embedding,
            n_results=n_results
        )

        # Step 3: Extract documents
        documents = results.get("documents", [[]])[0]

        # Step 4: Extract metadata
        metadatas = results.get("metadatas", [[]])[0]

        # If no relevant chunks are found
        if not documents:
            return {
                "found": False,
                "context": "No relevant information found.",
                "sources": []
            }

        # Combine only the top relevant chunks
        context = "\n\n".join(documents)

        # Get unique source names
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


def search_project_knowledge(question, n_results=1):
    """
    Search project knowledge using the RAG pipeline.
    This function is used by the Support Agent.
    """

    rag = RAGEngine()

    return rag.search(
        question=question,
        n_results=n_results
    )