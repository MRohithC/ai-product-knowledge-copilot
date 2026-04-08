from langchain_core.documents import Document
import re

STOP_WORDS = {
    "what", "is", "the", "a", "an", "right", "now", "tell", "me", "about",
    "give", "show", "please", "how", "when", "where", "why", "are", "do",
    "does", "did", "can", "could", "would", "should"
}


def load_documents():
    with open("data/product_docs.txt", "r", encoding="utf-8") as f:
        text = f.read()

    return [Document(page_content=text, metadata={"source": "product_docs.txt"})]


DOCS = load_documents()


def tokenize(text: str):
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())
    return [w for w in words if w not in STOP_WORDS and len(w) > 2]


def simple_retriever(query: str):
    query_words = set(tokenize(query))
    if not query_words:
        return []

    results = []

    for doc in DOCS:
        doc_words = set(tokenize(doc.page_content))
        overlap = query_words.intersection(doc_words)

        if len(overlap) >= 1:
            results.append((doc, len(overlap)))

    results.sort(key=lambda x: x[1], reverse=True)

    return [doc for doc, score in results[:3]]