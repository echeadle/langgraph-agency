# Phase 5: RAG Integration

This phase focuses on integrating a Retrieval-Augmented Generation (RAG) system into the multi-agent setup. This will allow agents to store and retrieve information from a persistent knowledge base, enhancing their ability to inform their work with relevant context.

## Objectives

- Integrate a vector store (e.g., FAISS or ChromaDB) to create a persistent knowledge base.
- Develop a mechanism for agents to add information from their research to the knowledge base.
- Develop a mechanism for agents to retrieve information from the knowledge base for future tasks.

## `rag.py` Code

```python
import os
from langchain_community.vectorstores import Chroma
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
```

## Updated `planner.py` Code

```python
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class Planner:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a planner. Your job is to take a research summary and any retrieved context to create a detailed, step-by-step development plan.\n\nRetrieved Context: {context}"),
                ("user", "Research Summary: {summary}"),
            ]
        )
        self.chain = self.prompt | self.llm

    def plan(self, summary: str, context: str = "") -> str:
        message = self.chain.invoke({"summary": summary, "context": context})
        return getattr(message, "content", str(message))

if __name__ == "__main__":
    planner = Planner()
    # This is a placeholder summary for testing purposes
    test_summary = "LangGraph is a library for building language agent applications with a graph-based approach. It allows for complex agentic workflows, state management, and human-in-the-loop interactions."
    plan = planner.plan(test_summary)
    print(plan)
```

## Updated `main.py` Code (Orchestration with RAG Integration)

This updated `main.py` integrates the RAG system. The `research_node` now adds research summaries to the knowledge base, and the `plan_node` retrieves relevant information from the knowledge base to inform the planning process.

```python
from typing import TypedDict, Annotated, List, NotRequired
import io
from PIL import Image as PILImage
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, END
from researcher import Researcher
from planner import Planner
from coder import Coder
from tester import Tester
from rag import RAG
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    research_summary: NotRequired[str]
    plan: NotRequired[str]
    user_input: str
    chat_history: Annotated[List[BaseMessage], "append"]
    approved: NotRequired[bool]
    code_output: NotRequired[str]
    test_output: NotRequired[str]
    retrieved_documents: NotRequired[List[str]]

# Initialize agents
researcher_agent = Researcher()
planner_agent = Planner()
coder_agent = Coder()
tester_agent = Tester()
rag_agent = RAG()

def research_node(state: AgentState):
    print("---RESEARCHING---")
    research_summary = researcher_agent.research(state["user_input"])
    rag_agent.add_to_knowledge_base(research_summary, {"source": "research_summary"})
    return {"research_summary": research_summary}

def plan_node(state: AgentState):
    print("---PLANNING---")
    retrieved_docs = rag_agent.retrieve_from_knowledge_base(state["research_summary"])
    retrieved_content = "\n".join([doc.page_content for doc in retrieved_docs])
    plan = planner_agent.plan(state["research_summary"], retrieved_content)
    return {"plan": plan, "retrieved_documents": [doc.page_content for doc in retrieved_docs]}

def human_approval_node(state: AgentState):
    print("---AWAITING HUMAN APPROVAL---")
    print(f"Generated Plan:\n{state['plan']}")
    # In a real application, this would involve a user interface or a more sophisticated approval mechanism.
    # For now, we'll simulate human approval via direct input.
    while True:
        approval = input("Do you approve this plan? (yes/no): ").lower()
        if approval in ["yes", "no"]:
            break
        else:
            print("Invalid input. Please type 'yes' or 'no'.")
    return {"approved": approval == "yes"}

def code_node(state: AgentState):
    print("---CODING---")
    code_output = coder_agent.code(state["plan"])
    return {"code_output": code_output}

def test_node(state: AgentState):
    print("---TESTING---")
    test_output = tester_agent.test(state["code_output"])
    return {"test_output": test_output}

def draw_graph(graph):
    """
    Generates and displays a diagram of the graph.
    """
    try:
        img_data = graph.get_graph().draw_mermaid_png()
        image = PILImage.open(io.BytesIO(img_data))
        image.show()
    except Exception as e:
        print(f"Error drawing graph: {e}")

# Build the graph
workflow = StateGraph(AgentState)

workflow.add_node("research", research_node)
workflow.add_node("plan", plan_node)
workflow.add_node("human_approval", human_approval_node)
workflow.add_node("code", code_node)
workflow.add_node("test", test_node)

workflow.set_entry_point("research")

workflow.add_edge("research", "plan")
workflow.add_edge("plan", "human_approval")

workflow.add_conditional_edges(
    "human_approval",
    lambda state: "code" if state["approved"] else "plan", # If approved, go to code. Otherwise, go back to plan for revision (simplified for now).
    {"code": "code", "plan": "plan"}
)

workflow.add_edge("code", "test")
workflow.add_edge("test", END)

app = workflow.compile()

if __name__ == "__main__":
    draw_option = input("Do you want to draw the graph? (yes/no): ").lower()
    if draw_option == "yes":
        draw_graph(app)

    user_query = input("What would you like to research and plan?: ")
    inputs: AgentState = {"user_input": user_query, "chat_history": []}
    for s in app.stream(inputs):
        print(s)
```