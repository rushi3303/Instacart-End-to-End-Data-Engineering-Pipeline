from pathlib import Path


# Get the path of the documents folder
DOCUMENTS_DIR = Path(__file__).parent / "documents"


def load_documents():
    """
    Load all .txt documents from the documents folder.

    Returns:
        list[dict]: List containing document name and content.
    """

    documents = []

    # Check if documents folder exists
    if not DOCUMENTS_DIR.exists():
        print("Documents folder not found.")
        return documents

    # Read all .txt files
    for file_path in DOCUMENTS_DIR.glob("*.txt"):

        try:
            content = file_path.read_text(
                encoding="utf-8"
            )

            documents.append(
                {
                    "source": file_path.name,
                    "content": content
                }
            )

        except Exception as error:
            print(f"Error loading {file_path.name}: {error}")

    return documents