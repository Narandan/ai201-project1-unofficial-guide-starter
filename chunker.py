def chunk_text(text, source, chunk_size=400, overlap=50):
    """Split text into chunks of chunk_size characters with overlap.
    Returns a list of dicts with 'text', 'source', and 'chunk_index' keys."""
    chunks = []
    start = 0
    chunk_index = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if len(chunk) > 0:
            chunks.append({
                "text": chunk,
                "source": source,
                "chunk_index": chunk_index
            })
            chunk_index += 1

        start = end - overlap

    return chunks


def chunk_all_documents(documents):
    """Chunk all documents and return a flat list of all chunks."""
    all_chunks = []

    for doc in documents:
        doc_chunks = chunk_text(doc["text"], doc["source"])
        all_chunks.extend(doc_chunks)

    return all_chunks


if __name__ == "__main__":
    from ingest import load_documents

    docs = load_documents()
    chunks = chunk_all_documents(docs)

    print(f"\nTotal chunks: {len(chunks)}")
    print("\n--- 5 SAMPLE CHUNKS ---")
    
    import random
    for chunk in random.sample(chunks, 5):
        print(f"\nSource: {chunk['source']} | Index: {chunk['chunk_index']}")
        print(f"{chunk['text']}")
        print("-" * 60)