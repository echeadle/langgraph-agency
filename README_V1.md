# Phase 1: The Researcher Agent

This phase focuses on creating a single agent that can research a topic using the Tavily Search tool and provide a summary of its findings.

## Implementation

- A `researcher.py` file was created to house the researcher agent.
- The agent is built using LangChain and utilizes the `ChatOpenAI` model.
- It's equipped with the `TavilySearchResults` tool to perform web searches.
- The agent takes a topic as input, researches it, and returns a summary.
