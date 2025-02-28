from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from typing import List, Optional
import tiktoken

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
        try:
            # Initialize with comprehensive CDP documentation samples
            sample_docs = [
                """Segment Documentation (https://segment.com/docs/?ref=nav):
                To set up a new source in Segment:
                1. Log in to your Segment workspace
                2. Navigate to the Sources section in the left sidebar
                3. Click 'Add Source' button at the top right
                4. Search for or select your desired platform/source type
                5. Follow the source-specific setup instructions
                6. Configure your source settings and API keys
                7. Enable the source when ready
                8. Verify data flow in the Segment debugger""",

                """mParticle Documentation (https://docs.mparticle.com/):
                Creating user profiles in mParticle:
                1. Set up the mParticle SDK in your application
                2. Implement user identification calls
                3. Add custom user attributes
                4. Track user events and behaviors
                5. Configure identity mapping
                6. Set up audience rules
                7. Monitor user profiles in the dashboard""",

                """Lytics Documentation (https://docs.lytics.com/):
                Building audience segments in Lytics:
                1. Access the Audience Builder section
                2. Create a new segment
                3. Define behavioral criteria
                4. Set up user attributes
                5. Configure frequency and recency rules
                6. Test your segment criteria
                7. Activate the segment for use""",

                """Zeotap Documentation (https://docs.zeotap.com/home/en-us/):
                Data integration with Zeotap:
                1. Access the Data Sources section
                2. Set up your data source connection
                3. Configure data mapping rules
                4. Set up identity resolution
                5. Validate data quality
                6. Monitor data ingestion
                7. Create unified customer profiles"""
            ]

            texts = self.text_splitter.split_text("\n".join(sample_docs))
            self.doc_store = FAISS.from_texts(texts, self.embeddings)
            print("Successfully initialized document store")

        except Exception as e:
            print(f"Error initializing document store: {str(e)}")
            self.doc_store = None

    def get_relevant_docs(self, query: str, k: int = 2) -> Optional[str]:
        try:
            if not self.doc_store:
                return None

            docs = self.doc_store.similarity_search(query, k=k)
            return "\n".join([doc.page_content for doc in docs])

        except Exception as e:
            print(f"Error retrieving relevant docs: {str(e)}")
            return None