import re


def split_text(text, chunk_size=500, overlap=100):
    """
    Split a section into smaller chunks only if
    the section is larger than chunk_size.
    """

    # If section is small enough, keep it as one chunk
    if len(text) <= chunk_size:
        return [text.strip()]

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        # Stop if we reached the end
        if end >= text_length:
            break

        start = end - overlap

    return chunks


def split_by_sections(text):
    """
    Split project knowledge using section headings.

    Example:

    [BRONZE LAYER]
    content...

    [SILVER LAYER]
    content...

    Each heading and its content remain together.
    """

    pattern = r"(?=^\[[^\]]+\])"

    sections = re.split(
        pattern,
        text,
        flags=re.MULTILINE
    )

    return [
        section.strip()
        for section in sections
        if section.strip()
    ]


def chunk_documents(documents, chunk_size=500, overlap=100):
    """
    Create chunks for all loaded documents.

    First:
        Split document by section headings.

    Then:
        If a section is larger than chunk_size,
        split that section into smaller overlapping chunks.
    """

    all_chunks = []

    for document in documents:

        source = document["source"]
        content = document["content"]

        # Step 1: Split document into logical sections
        sections = split_by_sections(content)

        chunk_index = 0

        # Step 2: Split large sections if necessary
        for section in sections:

            section_chunks = split_text(
                section,
                chunk_size,
                overlap
            )

            for chunk in section_chunks:

                all_chunks.append(
                    {
                        "id": f"{source}_chunk_{chunk_index}",
                        "source": source,
                        "content": chunk
                    }
                )

                chunk_index += 1

    return all_chunks