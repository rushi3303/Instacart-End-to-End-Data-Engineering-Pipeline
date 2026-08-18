from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Converts document chunks into vector embeddings.
    """

    def __init__(self):
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def create_embedding(self, text):
        """
        Convert a single text into an embedding vector.
        """

        embedding = self.model.encode(text)

        return embedding.tolist()

    def create_embeddings(self, chunks):
        """
        Convert multiple document chunks into embeddings.

        Each chunk is expected to be a dictionary like:

        {
            "id": "...",
            "content": "...",
            "source": "..."
        }
        """

        # Extract ONLY text content from chunks
        texts = [
            chunk["content"]
            for chunk in chunks
        ]

        embeddings = self.model.encode(
            texts,
            show_progress_bar=False
        )

        return embeddings.tolist()