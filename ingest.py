import os
import re

DOCUMENTS_DIR = "documents"

def clean_text(text):
    # Remove Reddit interaction lines (catch all variations)
    text = re.sub(r'\bUpvote\b', '', text)
    text = re.sub(r'\bDownvote\b', '', text)
    text = re.sub(r'\bAward\b', '', text)
    text = re.sub(r'\bShare\b', '', text)
    text = re.sub(r'\bReply\b', '', text)
    text = re.sub(r'\bavatar\b', '', text)

    # Remove standalone numbers (vote counts)
    text = re.sub(r'^\d+$', '', text, flags=re.MULTILINE)
    # Remove Reddit user references
    text = re.sub(r'u/\w+', '', text)
    # Remove bullet separators
    text = re.sub(r'^\s*•\s*$', '', text, flags=re.MULTILINE)
    # Remove RMP thumbs counts
    text = re.sub(r'Thumbs up\n?\d*\n?Thumbs down\n?\d*', '', text)
    # Remove excessive blank lines
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    return text.strip()

def load_documents():
    """Load all .txt files from the documents folder.
    Returns a list of dicts with 'source' and 'text' keys."""
    documents = []
    
    for filename in os.listdir(DOCUMENTS_DIR):
        if filename.endswith(".txt"):
            filepath = os.path.join(DOCUMENTS_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            
            text = clean_text(text)  # ← now actually called
            
            documents.append({
                "source": filename,
                "text": text
            })
            print(f"Loaded: {filename} ({len(text)} characters)")
    
    return documents

if __name__ == "__main__":
    docs = load_documents()
    print(f"\nTotal documents loaded: {len(docs)}")