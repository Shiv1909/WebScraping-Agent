# agent/chunker.py

from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict

class TextChunker:
    def __init__(self, chunk_size: int = 2048, chunk_overlap: int = 512):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", "!", "?", " ", ""]
        )

    def chunk_text(self, content: str, metadata: Dict[str, str]) -> List[Dict[str, str]]:
        """
        Split the text into chunks and attach metadata for vector storage.

        Args:
            content (str): Raw text content.
            metadata (Dict[str, str]): Metadata like URL, title, etc.

        Returns:
            List[Dict[str, str]]: List of chunks with metadata.
        """
        chunks = self.splitter.split_text(content)
        return [{"content": chunk, "metadata": metadata} for chunk in chunks]
