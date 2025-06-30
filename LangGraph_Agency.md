# Project: LangGraph AI Agency

## Vision

Build a modular, multi-agent system using LangGraph that can autonomously deliver Python applications—encompassing research, planning, coding, testing, and delivery. The project structure should reflect clear separation of concerns and promote maintainability and scalability.

---

## Why a Good Directory Structure?

- **Clarity:** Separation by responsibility (agents, tools, workflows) makes the system easy to navigate and maintain.
- **Testability:** Isolates tests and core logic for better CI/CD and quality control.
- **Extensibility:** New agents or tools can be added cleanly.
- **Reusability:** Core modules and shared resources are modular.

---

## Recommended Project Directory Structure

```text
langgraph_agency/
├── agents/
│   ├── researcher.py
│   ├── planner.py
│   ├── coder.py
│   ├── tester.py
│   └── __init__.py
├── workflows/
│   ├── orchestrator.py
│   ├── human_in_loop.py
│   └── __init__.py
├── tools/
│   ├── tavily_search.py
│   └── __init__.py
├── rag/
│   ├── vectorstore.py
│   ├── knowledge_base.py
│   └── __init__.py
├── tests/
│   ├── test_agents.py
│   ├── test_tools.py
│   └── test_workflows.py
├── config/
│   └── settings.py
├── main.py
├── requirements.txt
└── README.md
```

**Explanation:**

- `agents/`: Encapsulates the logic for each agent (SRP — Single Responsibility Principle).
- `workflows/`: Handles orchestration and interaction logic, including human-in-the-loop approval.
- `tools/`: Integrates external APIs and utilities.
- `rag/`: Modules to manage RAG (vector store, retrieval, ingestion).
- `tests/`: Test modules mapped to the code base for high code quality.
- `config/`: Central location for configuration and secrets.
- `main.py`: Entry point for running the orchestration.
- `requirements.txt` and `README.md`: Standard best practices for dependency and project documentation.

---

## Detailed, Improved Roadmap

### Phase 1: Bootstrapping & The Researcher Agent

- **What:** Initialize repo, implement `agents/researcher.py` with Tavily Search tool from `tools/tavily_search.py`.
- **Why:** Establishes a baseline for tool-wrapping and agent interfaces.
- **How:** Scaffold project as above; researcher agent accepts user brief and returns a summary.
- **Artifacts:** Pre-populate `requirements.txt` and basic test for agent.

### Phase 2: Planner Agent & Human-in-the-Loop Workflow

- **What:** Implement `agents/planner.py` to transform the researcher's summaries into actionable, step-by-step project plans. Build this as a pure agent-to-agent handoff.
- **Why:** Ensures a clear modular flow between agents and enables easier testing and debugging of the agent pipeline.
- **How:** Develop the planner agent to accept the researcher's output and return a structured project plan. Write unit tests to verify output quality and integration tests for the agent pipeline (Researcher → Planner).
- **Defer** any CLI, approval, or human-in-the-loop logic to a later phase, marking clearly in the code or documentation where the approval step will eventually be inserted.

### Phase 3: Coder Agent

- **What:** `agents/coder.py` generates Python code from the approved plan.
- **Why:** Encapsulates transformation of plan to code as a pure agent responsibility.
- **How:** Ensure modularity—code artifacts are saved in a `generated/` directory or returned as structured output. Write automated tests for generated script syntactic validity.

### Phase 4: Tester Agent

- **What:** `agents/tester.py` for generating and running tests.
- **Why:** Testing should be automated and separate for maintainability.
- **How:** For now, mock test execution (per your no-code-execution rule); agent produces test code and a "dummy" result. Future: Integrate a sandbox for actual test execution.

### Phase 5: RAG Integration

- **What:** Create `rag/` modules, integrate a vector database, and agent for data ingestion/retrieval.
- **Why:** Knowledge retention drastically improves research, coding, and automated documentation.
- **How:** Agents query vectorstore in parallel with live research. Add sample workflows using RAG.

### Phase 6: Orchestration and Workflow Management

- **What:** Implement master orchestrator in `workflows/orchestrator.py` to manage agent execution order and data flow.
- **Why:** Orchestration is critical for manageable, extendable agent systems.
- **How:** Define clear state transitions and message passing protocols. Add an integration test in `tests/test_workflows.py`.

---

## Additional Best Practices for Project Robustness

- **Logging:** Implement structured logging at agent/workflow levels for traceability.
- **Configuration:** Use `config/settings.py` for API keys, environment flags, and parameters.
- **Documentation:** Maintain clear function/module-level docstrings.
- **Incremental CI:** For each phase, ensure minimal test coverage.

---

## Summary Table of Improvements

| Area                       | Original      | Improved                         | Rationale                           |
| -------------------------- | ------------- | -------------------------------- | ----------------------------------- |
| Project structure          | Not specified | Modular, layered                 | Maintainability, scaling            |
| Test coverage              | Not mentioned | Unit/integration tests per phase | Code quality, easier refactoring    |
| Human-in-the-loop location | Not specified | Workflows/                       | Clean separation agent <-> workflow |
| Logging/config             | Not mentioned | Centralized modules              | Traceability, config reuse          |
| RAG integration            | General       | Isolated rag/ module             | Plug-and-play, testable             |
| Code artifact handling     | Not clear     | `/generated` dir                 | Easy output management              |

---

## Suggested Next Steps

1. **Scaffold the directory structure.** Commit the layout and add README with overall architecture.
2. **Fill in agent interfaces (Phase 1).** Start with `researcher.py` and its test.
3. **Iterate through roadmap.** Build and test one phase at a time.
4. **Regularly refactor and maintain documentation.**
