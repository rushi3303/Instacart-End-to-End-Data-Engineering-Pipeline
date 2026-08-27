from pathlib import Path
from agent.rag.build_index import build_index


DOCUMENT_FILE = (
    Path(__file__).parent
    / "documents"
    / "project_knowledge.txt"
)

TIMESTAMP_FILE = (
    Path(__file__).parent
    / "documents"
    / ".index_timestamp"
)


def check_and_update_index():
    """
    Checks whether project_knowledge.txt has changed.

    If the document is new or modified, rebuilds
    the RAG vector index.
    """

    # Document does not exist
    if not DOCUMENT_FILE.exists():
        print("RAG document not found.")
        return

    current_timestamp = DOCUMENT_FILE.stat().st_mtime

    # First time
    if not TIMESTAMP_FILE.exists():

        print("RAG index not initialized.")
        print("Building RAG index...")

        build_index()

        TIMESTAMP_FILE.write_text(
            str(current_timestamp),
            encoding="utf-8"
        )

        print("RAG index initialized.")
        return

    # Read previous timestamp
    try:

        previous_timestamp = float(
            TIMESTAMP_FILE.read_text(
                encoding="utf-8"
            ).strip()
        )

    except Exception:

        previous_timestamp = 0

    # Check whether document changed
    if current_timestamp != previous_timestamp:

        print("Project knowledge changed.")
        print("Rebuilding RAG index...")

        build_index()

        TIMESTAMP_FILE.write_text(
            str(current_timestamp),
            encoding="utf-8"
        )

        print("RAG index updated.")

    else:

        print("RAG knowledge is already up to date.")