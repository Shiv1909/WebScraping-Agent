# pipeline/embed_and_store.py

from langchain.schema import Document
from langchain.vectorstores import Chroma
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def embed_and_store_chunks(all_chunks, embedding_model, persist_dir="chroma_store"):
    """
    Embeds all chunks using the embedding model and saves to Chroma.
    """
    embedded_chunks = []

    for chunk in all_chunks:
        try:
            vector = embedding_model.embed_query(chunk["content"])
            embedded_chunks.append({
                "embedding": vector,
                "content": chunk["content"],
                "metadata": chunk["metadata"]
            })
        except Exception as e:
            logger.warning(f"Failed to embed chunk: {e}")

    try:
        documents = [Document(page_content=chunk["content"], metadata=chunk["metadata"]) for chunk in embedded_chunks]
        chroma_store = Chroma.from_documents(
            documents=documents,
            embedding=embedding_model,
            persist_directory=persist_dir
        )
        chroma_store.persist()
        return chroma_store
    except Exception as e:
        logger.error(f"Failed to store embeddings in Chroma: {e}")
        return None
