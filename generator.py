import os
from groq import Groq
from dotenv import load_dotenv
from retriever import retrieve

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a helpful assistant for FSU Computer Science students.
Answer questions using ONLY the information provided in the documents below.
Do not use any outside knowledge or make assumptions beyond what is in the documents.
If the documents do not contain enough information to answer the question, say exactly:
"I don't have enough information in my sources to answer that question."
Always end your response with a "Sources:" section listing the document names you drew from."""

def generate_response(query):
    """Retrieve relevant chunks and generate a grounded response."""
    
    # Retrieve relevant chunks
    chunks = retrieve(query)
    
    # Build context from chunks
    context = ""
    sources = set()
    for chunk in chunks:
        context += f"\n---\n{chunk['text']}\n"
        sources.add(chunk['source'])
    
    # Build prompt
    user_prompt = f"""Documents:
{context}

Question: {query}

Answer using only the documents above. End with a Sources: section."""

    # Generate response
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=1000
    )

    answer = response.choices[0].message.content

    # Strip any LLM-generated sources section and add our own
    if "Sources:" in answer:
        answer = answer[:answer.index("Sources:")].strip()
    
    # Format clean source list
    source_list = "\n".join(f"• {s}" for s in sorted(sources))
    answer = f"{answer}\n\nSources:\n{source_list}"

    # Don't show sources if the system couldn't answer
    if "I don't have enough information" in answer:
        answer = answer.split("Sources:")[0].strip()
        answer += "\n\nSources: None — question is outside the scope of available documents."

    return {
        "answer": answer,
        "sources": list(sources),
        "chunks": chunks
    }

if __name__ == "__main__":
    test_queries = [
        "What do students say about David Gaitros's teaching style?",
        "Is attendance mandatory for Andy Wang's COP4610?",
        "Which FSU CS professors do students recommend most?",
        "What are students' biggest complaints about the FSU CS department?",
        "What do students say about Xin Yuan's course difficulty?"
    ]

    for query in test_queries:
        print(f"\nQUERY: {query}")
        print("=" * 60)
        result = generate_response(query)
        print(result["answer"])
        print()