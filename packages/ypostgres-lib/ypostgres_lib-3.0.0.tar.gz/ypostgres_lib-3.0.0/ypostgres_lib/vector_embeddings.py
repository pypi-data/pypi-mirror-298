from langchain_ollama import OllamaEmbeddings


def embed_text(text: str) -> list[float]:
    embeddings = OllamaEmbeddings(model="bge-m3")
    return embeddings.embed_query(text)
