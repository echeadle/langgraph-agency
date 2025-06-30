# Phase 3: The Coder Agent

This phase introduces a new agent, the "Coder," responsible for generating Python code based on the approved plan from the Planner agent.

## Objectives

- Create a "Coder" agent capable of generating Python code.
- Integrate the Coder agent into the existing workflow, following the human approval step.

## `coder.py` Code

```python
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class Coder:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a coder. Your job is to take a detailed development plan and generate Python code that implements the plan. Provide only the code, no explanations or extra text."),
                ("user", "Development Plan: {plan}"),
            ]
        )
        self.chain = self.prompt | self.llm

    def code(self, plan: str) -> str:
        message = self.chain.invoke({"plan": plan})
        return getattr(message, "content", str(message))

if __name__ == "__main__":
    coder = Coder()
    # This is a placeholder plan for testing purposes
    test_plan = "Create a Python function that takes two numbers and returns their sum."
    code_output = coder.code(test_plan)
    print(code_output)
```

## Updated `main.py` Code (Orchestration with Coder Agent and Graph Drawing)

This updated `main.py` integrates the Coder agent into the workflow and adds a function to draw the graph, giving the user an option to visualize the workflow.

```python
from typing import TypedDict, Annotated, List, NotRequired
import io
from PIL import Image as PILImage
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, END
from researcher import Researcher
from planner import Planner
from coder import Coder
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    research_summary: NotRequired[str]
    plan: NotRequired[str]
    user_input: str
    chat_history: Annotated[List[BaseMessage], "append"]
    approved: NotRequired[bool]
    code_output: NotRequired[str]

# Initialize agents
researcher_agent = Researcher()
planner_agent = Planner()
coder_agent = Coder()

def research_node(state: AgentState):
    print("---RESEARCHING---")
    research_summary = researcher_agent.research(state["user_input"])
    return {"research_summary": research_summary}

def plan_node(state: AgentState):
    print("---PLANNING---")
    plan = planner_agent.plan(state["research_summary"])
    return {"plan": plan}

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

workflow.set_entry_point("research")

workflow.add_edge("research", "plan")
workflow.add_edge("plan", "human_approval")

workflow.add_conditional_edges(
    "human_approval",
    lambda state: "code" if state["approved"] else "plan", # If approved, go to code. Otherwise, go back to plan for revision (simplified for now).
    {"code": "code", "plan": "plan"}
)

workflow.add_edge("code", END)

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
