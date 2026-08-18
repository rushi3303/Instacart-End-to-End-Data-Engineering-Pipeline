import chromadb


class VectorStore:
    """
    Stores document chunks and their embeddings
    in ChromaDB.
    """

    def __init__(self):
        # Create persistent ChromaDB database
        self.client = chromadb.PersistentClient(
            path="agent/rag/chroma_db"
        )

        # Create or load collection
        self.collection = self.client.get_or_create_collection(
            name="project_knowledge"
        )

    def add_documents(self, chunks, embeddings):
        """
        Stores chunks and embeddings in ChromaDB.

        Each chunk contains:
        - id
        - content
        - source
        """

        # Extract IDs
        ids = [
            chunk["id"]
            for chunk in chunks
        ]

        # Extract ONLY text content
        documents = [
            chunk["content"]
            for chunk in chunks
        ]

        # Store source as metadata
        metadatas = [
            {
                "source": chunk["source"]
            }
            for chunk in chunks
        ]

        # Store everything in ChromaDB
        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def search(self, query_embedding, n_results=3):
        """
        Searches for the most relevant document chunks.
        """

        results = self.collection.query(
            query_embeddings=[
                query_embedding
            ],
            n_results=n_results
        )

        return results

    def get_document_count(self):
        """
        Returns total number of chunks
        stored in ChromaDB.
        """

        return self.collection.count()