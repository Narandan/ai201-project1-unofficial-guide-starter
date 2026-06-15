import chromadb
from sentence_transformers import SentenceTransformer

COLLECTION_NAME = "unofficial_guide"

def get_collection():
    client = chromadb.PersistentClient(path="chroma_db")
    return client.get_collection(COLLECTION_NAME)

def retrieve(query, k=5):
    """Retrieve top-k chunks most relevant to the query."""
    model = SentenceTransformer("all-MiniLM-L6-v2")
    collection = get_collection()

    query_embedding = model.encode([query])[0].tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )

    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": round(results["distances"][0][i], 4)
        })

    return chunks

if __name__ == "__main__":
    test_queries = [
        "What do students say about David Gaitros's teaching style?",
        "Is attendance mandatory for Andy Wang's COP4610?",
        "What are students' biggest complaints about the FSU CS department?"
    ]

    for query in test_queries:
        print(f"\nQUERY: {query}")
        print("-" * 60)
        chunks = retrieve(query)
        for chunk in chunks:
            print(f"Source: {chunk['source']} | Distance: {chunk['distance']}")
            print(f"{chunk['text'][:200]}")
            print()