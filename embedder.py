import chromadb
from sentence_transformers import SentenceTransformer
from ingest import load_documents
from chunker import chunk_all_documents

COLLECTION_NAME = "unofficial_guide"

def embed_and_store():
    """Embed all chunks and store them in ChromaDB with source metadata."""
    
    # Load and chunk documents
    print("Loading documents...")
    docs = load_documents()
    chunks = chunk_all_documents(docs)
    print(f"Total chunks to embed: {len(chunks)}")

    # Load embedding model
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Set up ChromaDB
    client = chromadb.PersistentClient(path="chroma_db")
    
    # Delete existing collection if it exists (for re-runs)
    try:
        client.delete_collection(COLLECTION_NAME)
    except:
        pass
    
    collection = client.create_collection(COLLECTION_NAME)

    # Embed and store in batches
    print("Embedding and storing chunks...")
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)

    collection.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        embeddings=embeddings.tolist(),
        documents=texts,
        metadatas=[{"source": chunk["source"], "chunk_index": chunk["chunk_index"]} 
                   for chunk in chunks]
    )

    print(f"\nStored {collection.count()} chunks in ChromaDB.")
    return collection

if __name__ == "__main__":
    embed_and_store()