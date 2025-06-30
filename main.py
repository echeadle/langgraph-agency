import os
from typing import TypedDict, Annotated, List, NotRequired
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, END
from agents.researcher import Researcher
from agents.planner import Planner
from agents.coder import Coder
from agents.tester import Tester
from agents.rag import RAG
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Prompt

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
    feedback: NotRequired[str]
    project_name: NotRequired[str]

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
    project_md_path = os.path.join("output", state["project_name"], "project.md")
    try:
        with open(project_md_path, "r") as f:
            project_context = f.read()
    except FileNotFoundError:
        project_context = "No project.md file found."
    rag_agent.add_to_knowledge_base(project_context, {"source": "project.md"})
    retrieved_docs = rag_agent.retrieve_from_knowledge_base(state["research_summary"])
    retrieved_content = "\n".join([doc.page_content for doc in retrieved_docs])
    full_context = f"Project Context from project.md:\n{project_context}\n\nRetrieved Documents:\n{retrieved_content}"
    plan = planner_agent.plan(
        summary=state["research_summary"],
        context=full_context,
        feedback=state.get("feedback", "No feedback provided."),
    )
    return {"plan": plan, "retrieved_documents": [doc.page_content for doc in retrieved_docs]}

def human_approval_node(state: AgentState):
    console = Console()
    console.print("[bold yellow]---AWAITING HUMAN APPROVAL---[/bold yellow]")
    console.print(f"Generated Plan:\n{state['plan']}")
    
    approval = Prompt.ask("Do you approve this plan?", choices=["yes", "no"], default="yes")
    
    if approval == "yes":
        return {"approved": True}
    else:
        feedback = Prompt.ask("Please provide your feedback")
        return {"approved": False, "feedback": feedback}

def code_node(state: AgentState):
    print("---CODING---")
    code_output = coder_agent.code(state["plan"])
    project_path = os.path.join("output", state["project_name"])
    with open(os.path.join(project_path, "code.py"), "w") as f:
        f.write(code_output)
    return {"code_output": code_output}

def test_node(state: AgentState):
    print("---TESTING---")
    test_output = tester_agent.test(state["code_output"])
    project_path = os.path.join("output", state["project_name"])
    with open(os.path.join(project_path, "tests.py"), "w") as f:
        f.write(test_output)
    return {"test_output": test_output}

def draw_graph(graph):
    """
    Prints a text-based representation of the graph to the console.
    """
    console = Console()
    console.print("[bold cyan]Graph Structure:[/bold cyan]")
    for node in graph.nodes:
        console.print(f"- [bold green]Node:[/bold green] {node}")
        for edge in graph.edges:
            if edge.source == node:
                console.print(f"  - [bold blue]Edge to:[/bold blue] {edge.target}")

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
    console = Console()
    project_name = Prompt.ask("Enter the project name")
    project_path = os.path.join("output", project_name)
    os.makedirs(project_path, exist_ok=True)
    project_md_content = Prompt.ask(f"Provide initial instructions for `{project_name}/project.md` (optional)")
    with open(os.path.join(project_path, "project.md"), "w") as f:
        f.write(project_md_content)
    draw_option = Prompt.ask("Do you want to draw the graph?", choices=["yes", "no"], default="no")
    if draw_option == "yes":
        draw_graph(app.graph)
    user_query = Prompt.ask("What would you like to research and plan for this project?")
    inputs: AgentState = {"user_input": user_query, "chat_history": [], "project_name": project_name}
    for s in app.stream(inputs):
        console.print(s)
    final_state = app.invoke(inputs)
    console.print("\n[bold green]--- FINAL RESULTS ---[/bold green]")
    console.print(f"[bold]Research Summary:[/bold] {final_state.get('research_summary')}")
    console.print(f"[bold]Development Plan:[/bold] {final_state.get('plan')}")
    console.print(f"[bold]Generated Code:[/bold] {final_state.get('code_output')}")
    console.print(f"[bold]Generated Tests:[/bold] {final_state.get('test_output')}")
