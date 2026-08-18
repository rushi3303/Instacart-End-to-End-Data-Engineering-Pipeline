from agent.rag.document_loader import load_documents
from agent.rag.chunker import chunk_documents
from agent.rag.embedding_service import EmbeddingService
from agent.rag.vector_store import VectorStore


def build_index():
    """
    Builds the RAG vector database.

    Flow:
    1. Load project documents
    2. Split documents into chunks
    3. Convert chunks into embeddings
    4. Store embeddings in ChromaDB
    """

    print("\nStarting RAG Index Build...\n")

    # =====================================
    # STEP 1: LOAD DOCUMENTS
    # =====================================

    documents = load_documents()

    print(f"Documents loaded: {len(documents)}")

    # =====================================
    # STEP 2: CREATE CHUNKS
    # =====================================

    chunks = chunk_documents(
        documents,
        chunk_size=500,
        overlap=100
    )

    print(f"Chunks created: {len(chunks)}")

    # =====================================
    # STEP 3: CREATE EMBEDDINGS
    # =====================================

    embedding_service = EmbeddingService()

    embeddings = embedding_service.create_embeddings(
        chunks
    )

    print(f"Embeddings created: {len(embeddings)}")

    # =====================================
    # STEP 4: STORE IN CHROMADB
    # =====================================

    vector_store = VectorStore()

    vector_store.add_documents(
        chunks,
        embeddings
    )

    print("\nRAG Vector Database Built Successfully!")

    print(f"Total chunks stored: {vector_store.get_document_count()}")


if __name__ == "__main__":
    build_index()