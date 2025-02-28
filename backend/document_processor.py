from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from typing import List, Optional, Dict
import tiktoken
import json

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        self.embeddings = OpenAIEmbeddings()
        self.doc_store = None
        self.initialize_docs()

    def initialize_docs(self):
        try:
            # Enhanced documentation samples with advanced use cases
            sample_docs = [
                """Segment Documentation (https://segment.com/docs/?ref=nav):
                Advanced Source Configuration:
                1. Custom Source Setup
                   - Define custom event schemas
                   - Configure event transformation rules
                   - Set up source-specific mappings
                2. Advanced Data Controls
                   - Implement data filtering rules
                   - Configure sampling rates
                   - Set up privacy controls
                3. Error Handling and Monitoring
                   - Configure retry policies
                   - Set up alerting rules
                   - Monitor data quality
                4. Integration Patterns
                   - Server-side vs client-side
                   - Mobile SDK implementation
                   - Cloud source configuration""",

                """mParticle Documentation (https://docs.mparticle.com/):
                Advanced Implementation Guide:
                1. Identity Resolution
                   - Cross-platform identity mapping
                   - Custom identity resolution rules
                   - Identity strategy configuration
                2. Data Planning
                   - Schema validation
                   - Data quality rules
                   - Version control
                3. Advanced SDK Features
                   - Offline data tracking
                   - Batch vs real-time processing
                   - Custom attribute handling
                4. Enterprise Features
                   - Multi-tenant architecture
                   - Role-based access control
                   - Audit logging""",

                """Lytics Documentation (https://docs.lytics.com/):
                Advanced Segmentation:
                1. Behavioral Scoring
                   - Custom scoring models
                   - Machine learning integration
                   - Predictive analytics
                2. Advanced Segment Rules
                   - Complex boolean logic
                   - Time-based conditions
                   - Multi-channel triggers
                3. Data Science Features
                   - Custom Python notebooks
                   - SQL query integration
                   - API automation
                4. Enterprise Scale
                   - High-volume processing
                   - Custom retention policies
                   - Advanced security controls""",

                """Zeotap Documentation (https://docs.zeotap.com/home/en-us/):
                Enterprise Integration:
                1. Data Governance
                   - Compliance frameworks
                   - Data privacy controls
                   - Audit trail setup
                2. Advanced Identity Resolution
                   - Probabilistic matching
                   - Custom identity graphs
                   - Cross-device tracking
                3. Machine Learning
                   - Custom model deployment
                   - Automated segmentation
                   - Predictive analytics
                4. Enterprise Features
                   - Multi-region setup
                   - Custom API endpoints
                   - Advanced monitoring"""
            ]

            texts = self.text_splitter.split_text("\n".join(sample_docs))
            self.doc_store = FAISS.from_texts(texts, self.embeddings)
            print("Successfully initialized document store with advanced documentation")

        except Exception as e:
            print(f"Error initializing document store: {str(e)}")
            self.doc_store = None

    def get_relevant_docs(self, query: str, k: int = 3) -> Optional[str]:
        try:
            if not self.doc_store:
                return None

            # Search with metadata
            docs = self.doc_store.similarity_search(query, k=k)

            # Format the results with section headers
            formatted_docs = []
            for doc in docs:
                content = doc.page_content.strip()
                if "Documentation" in content:
                    platform = content.split("Documentation")[0].strip()
                    formatted_docs.append(f"\n### {platform} Documentation ###\n{content}")
                else:
                    formatted_docs.append(content)

            return "\n".join(formatted_docs)

        except Exception as e:
            print(f"Error retrieving relevant docs: {str(e)}")
            return None