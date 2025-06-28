
import os
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_openai import ChatOpenAI

# Set up the Tavily Search tool
tavily_tool = TavilySearchResults(max_results=5)

# Define the researcher agent
class Researcher:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4-turbo-preview")
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a researcher. Your job is to research a topic and provide a summary of your findings."),
                ("user", "{topic}"),
            ]
        )
        self.chain = self.prompt | self.llm

    def research(self, topic: str) -> str:
        return self.chain.invoke({"topic": topic})

if __name__ == "__main__":
    researcher = Researcher()
    summary = researcher.research("What is LangGraph?")
    print(summary)
