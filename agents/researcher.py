
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
