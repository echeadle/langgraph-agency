# Phase 6: Agency Orchestration

This phase focuses on creating a master orchestrator or a new graph structure that manages the flow of information between all the agents, creating a seamless, end-to-end workflow.

## Objectives

- Create a master orchestrator to manage the flow between Researcher, Planner, Coder, and Tester agents.
- Ensure a seamless, end-to-end workflow for software development tasks.

## Directory Structure

The project now follows a more organized directory structure:

```
.env.sample
.gitignore
.python-version
GEMINI.md
LICENSE
main.py
pyproject.toml
README.md
.git/...
agents/
│   __init__.py
│   researcher.py
│   planner.py
│   coder.py
│   tester.py
│   rag.py
docs/
    README_V1.md
    README_V2.md
    README_V3.md
    README_V4.md
    README_V5.md
    README_V6.md
```

## Updated `main.py` Code (Orchestration with Final Results Display and New Imports)

This updated `main.py` includes a final output section that displays the research summary, development plan, generated code, and generated tests after the workflow completes. It also reflects the new import paths for the agents.

```python
from typing import TypedDict, Annotated, List, NotRequired
import io
from PIL import Image as PILImage
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, END
from agents.researcher import Researcher
from agents.planner import Planner
from agents.coder import Coder
from agents.tester import Tester
from agents.rag import RAG
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

    final_state = app.invoke(inputs)
    print("\n--- FINAL RESULTS ---")
    print(f"Research Summary: {final_state.get('research_summary')}")
    print(f"Development Plan: {final_state.get('plan')}")
    print(f"Generated Code: {final_state.get('code_output')}")
    print(f"Generated Tests: {final_state.get('test_output')}")
```

```