# Project: LangGraph Agency

## Vision

To create a multi-agent system built with LangGraph that can autonomously develop Python applications for a client. The agency will handle the entire software development lifecycle: from initial research and planning to coding, testing, and final delivery.

This project will serve as a comprehensive exploration of LangGraph's features, including state management, tool use, human-in-the-loop workflows, and multi-agent collaboration.

## Core Capabilities

- **Web Research**: Agents will use tools like Tavily Search to gather information and understand the client's requirements.
- **RAG (Retrieval-Augmented Generation)**: Agents will be able to store and retrieve information from a knowledge base (e.g., from books or documentation) to inform their work.
- **Planning**: An agent will be dedicated to creating a detailed development plan based on the research phase.
- **Client Approval**: The system will present the plan to the client for approval before proceeding (Human-in-the-loop).
- **Coding**: A specialized agent will write the Python code based on the approved plan.
- **Testing**: A dedicated testing agent will write and run tests to verify the code's functionality.

## Development Roadmap

We will build the agency incrementally, one agent and one feature at a time.

1.  **Phase 1: The Researcher Agent**
    -   Create a new LangGraph project structure.
    -   Build a single agent that can take a user request.
    -   Equip the agent with the Tavily Search tool.
    -   The agent should be able to research a topic and return a summary of its findings.

2.  **Phase 2: The Planner Agent & Human-in-the-Loop**
    -   Introduce a second agent that takes the researcher's output.
    -   This "Planner" agent will create a step-by-step development plan.
    -   Implement a human-in-the-loop step where the client must approve the plan before the process can continue.

3.  **Phase 3: The Coder Agent**
    -   Add a third agent specialized in writing Python code.
    -   This agent will take the approved plan and generate the corresponding Python script.

4.  **Phase 4: The Testing Agent**
    -   Add a fourth agent responsible for testing.
    -   This agent will analyze the generated code and create appropriate tests (e.g., using `pytest`).
    -   It will execute the tests and report the results.

5.  **Phase 5: RAG Integration**
    -   Integrate a vector store (e.g., FAISS or ChromaDB) to create a persistent knowledge base.
    -   Develop a mechanism for agents to add information from their research to the knowledge base and retrieve it in future tasks.

6.  **Phase 6: Agency Orchestration**
    -   Create a master orchestrator or a new graph structure that manages the flow of information between all the agents, creating a seamless, end-to-end workflow.
