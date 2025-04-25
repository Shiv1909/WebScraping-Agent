
from langchain.schema import Document
from langchain.vectorstores import Chroma

def embed_and_store_chunks(all_chunks, embedding_model, persist_dir="chroma_store"):
    embedded_chunks = []
    for chunk in all_chunks:
        vector = embedding_model.embed_query(chunk["content"])
        embedded_chunks.append({
            "embedding": vector,
            "content": chunk["content"],
            "metadata": chunk["metadata"]
        })

    documents = [Document(page_content=chunk["content"], metadata=chunk["metadata"]) for chunk in embedded_chunks]
    chroma_store = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=persist_dir
    )
    chroma_store.persist()
    return chroma_store
