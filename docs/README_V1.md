# Phase 1: The Researcher Agent

This phase focuses on creating a single agent that can research a topic using the Tavily Search tool and provide a summary of its findings.

## Implementation

- A `researcher.py` file was created to house the researcher agent.
- The agent is built using LangChain and utilizes the `ChatOpenAI` model.
- It's equipped with the `TavilySearch` tool to perform web searches.
- The agent takes a topic as input, researches it, and returns a summary.
- Ensure you have a `.env` file with your `OPENAI_API_KEY` and `TAVILY_API_KEY` set, as the script loads these environment variables.

## `researcher.py` Code

```python
import os
from langchain_tavily import TavilySearch
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Set up the Tavily Search tool
tavily_tool = TavilySearch(max_results=5)

# Define the researcher agent
class Researcher:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a researcher. Your job is to research a topic and provide a summary of your findings."),
                ("user", "{topic}"),
            ]
        )
        self.chain = self.prompt | self.llm

    def research(self, topic: str) -> str:
        message = self.chain.invoke({"topic": topic})
        return getattr(message, "content", str(message))

if __name__ == "__main__":
    researcher = Researcher()
    summary = researcher.research("What is LangGraph?")
    print(summary)
```