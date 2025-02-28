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
        # Initialize with more comprehensive CDP documentation samples
        sample_docs = [
            """Segment Documentation: To set up a new source in Segment:
            1. Navigate to the Sources section in your Segment workspace
            2. Click 'Add Source' and choose your platform
            3. Follow the integration guide for your specific source
            4. Configure the connection settings
            5. Enable the source and verify data flow""",

            """mParticle Documentation: Creating user profiles involves:
            1. Implementing the mParticle SDK
            2. Collecting user attributes and events
            3. Setting user identities
            4. Managing user consent
            5. Viewing user profiles in the dashboard""",

            """Lytics Documentation: Building audience segments requires:
            1. Accessing the Audience Builder
            2. Defining segment criteria
            3. Selecting behavioral triggers
            4. Setting audience rules
            5. Activating the segment""",

            """Zeotap Documentation: Data integration steps include:
            1. Setting up data sources
            2. Configuring data mappings
            3. Validating data quality
            4. Managing identity resolution
            5. Monitoring data flows"""
        ]

        try:
            texts = self.text_splitter.split_text("\n".join(sample_docs))
            self.doc_store = FAISS.from_texts(texts, self.embeddings)
        except Exception as e:
            print(f"Error initializing document store: {str(e)}")
            self.doc_store = None

    def get_relevant_docs(self, query: str, k: int = 3) -> Optional[str]:
        try:
            if not self.doc_store:
                return None

            docs = self.doc_store.similarity_search(query, k=k)
            return "\n".join([doc.page_content for doc in docs])
        except Exception as e:
            print(f"Error retrieving relevant docs: {str(e)}")
            return None