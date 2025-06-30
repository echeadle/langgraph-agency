
import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

class RAG:
    def __init__(self, collection_name="langgraph_agency_kb"):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
        self.vectorstore = Chroma(collection_name=collection_name, embedding_function=self.embeddings)

    def add_to_knowledge_base(self, text: str, metadata: dict = None):
        doc = Document(page_content=text, metadata=metadata or {})
        self.vectorstore.add_documents([doc])
        print(f"Added document to knowledge base: {text[:50]}...")

    def retrieve_from_knowledge_base(self, query: str, k: int = 3) -> list[Document]:
        docs = self.vectorstore.similarity_search(query, k=k)
        print(f"Retrieved {len(docs)} documents for query: {query}")
        return docs

if __name__ == "__main__":
    rag = RAG()
    rag.add_to_knowledge_base("LangGraph is a library for building language agent applications with a graph-based approach.", {"source": "LangGraph documentation"})
    rag.add_to_knowledge_base("The Planner agent creates a step-by-step development plan.", {"source": "Internal documentation"})

    results = rag.retrieve_from_knowledge_base("What is LangGraph?")
    for doc in results:
        print(f"- {doc.page_content} (Source: {doc.metadata.get("source", "N/A")})")
