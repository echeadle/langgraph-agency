# Phase 2: The Planner Agent & Human-in-the-Loop

This phase introduces a new agent, the "Planner," which takes the output from the Researcher agent and formulates a step-by-step development plan. A crucial aspect of this phase is the implementation of a human-in-the-loop mechanism, requiring client approval of the plan before further execution.

## Objectives

- Create a "Planner" agent capable of generating detailed development plans.
- Integrate the Planner agent to receive input from the Researcher agent.
- Implement a human-in-the-loop approval step for the generated plan.

## `planner.py` Code

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
                ("system", "You are a planner. Your job is to take a research summary and create a detailed, step-by-step development plan."),
                ("user", "Research Summary: {summary}"),
            ]
        )
        self.chain = self.prompt | self.llm

    def plan(self, summary: str) -> str:
        message = self.chain.invoke({"summary": summary})
        return getattr(message, "content", str(message))

if __name__ == "__main__":
    planner = Planner()
    # This is a placeholder summary for testing purposes
    test_summary = "LangGraph is a library for building language agent applications with a graph-based approach. It allows for complex agentic workflows, state management, and human-in-the-loop interactions."
    plan = planner.plan(test_summary)
    print(plan)
```

## `main.py` Code (Orchestration with Human-in-the-Loop)

This `main.py` file orchestrates the flow between the Researcher and Planner agents, incorporating a human approval step. It defines the graph structure, nodes, and edges for the workflow.

```python
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, END
from researcher import Researcher
from planner import Planner
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    research_summary: str
    plan: str
    user_input: str
    chat_history: Annotated[List[BaseMessage], "append"]

# Initialize agents
researcher_agent = Researcher()
planner_agent = Planner()

def research_node(state: AgentState):
    print("---RESEARCHING---")
    research_summary = researcher_agent.research(state["user_input"])
    return {"research_summary": research_summary}

def plan_node(state: AgentState):
    print("--PLANNING--")
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

# Build the graph
workflow = StateGraph(AgentState)

workflow.add_node("research", research_node)
workflow.add_node("plan", plan_node)
workflow.add_node("human_approval", human_approval_node)

workflow.set_entry_point("research")

workflow.add_edge("research", "plan")
workflow.add_edge("plan", "human_approval")

workflow.add_conditional_edges(
    "human_approval",
    lambda state: "end" if state["approved"] else "plan", # If approved, end. Otherwise, go back to plan for revision (simplified for now).
    {"end": END, "plan": "plan"}
)

app = workflow.compile()

if __name__ == "__main__":
    user_query = input("What would you like to research and plan?: ")
    inputs = {"user_input": user_query, "chat_history": []}
    for s in app.stream(inputs):
        print(s)
```