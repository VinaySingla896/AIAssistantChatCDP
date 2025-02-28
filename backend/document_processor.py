from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from typing import List, Optional

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.embeddings = OpenAIEmbeddings()
        self.doc_store = None
        self.initialize_docs()

    def initialize_docs(self):
        # This would typically load and process documentation from the CDPs
        # For now, we'll use placeholder text
        sample_docs = [
            "Segment Documentation: To set up a new source...",
            "mParticle Documentation: Creating user profiles...",
            "Lytics Documentation: Building audience segments...",
            "Zeotap Documentation: Data integration steps..."
        ]

        texts = self.text_splitter.split_text("\n".join(sample_docs))
        self.doc_store = FAISS.from_texts(texts, self.embeddings)

    def get_relevant_docs(self, query: str, k: int = 3) -> Optional[str]:
        if not self.doc_store:
            return None

        docs = self.doc_store.similarity_search(query, k=k)
        return "\n".join([doc.page_content for doc in docs])