
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
                ("system", "You are a planner. Your job is to take a research summary and any retrieved context to create a detailed, step-by-step development plan. If feedback is provided, incorporate it to revise the plan.\n\nRetrieved Context: {context}\n\nFeedback: {feedback}"),
                ("user", "Research Summary: {summary}"),
            ]
        )
        self.chain = self.prompt | self.llm

    def plan(self, summary: str, context: str = "", feedback: str = "No feedback provided.") -> str:
        message = self.chain.invoke({"summary": summary, "context": context, "feedback": feedback})
        return getattr(message, "content", str(message))

if __name__ == "__main__":
    planner = Planner()
    # This is a placeholder summary for testing purposes
    test_summary = "LangGraph is a library for building language agent applications with a graph-based approach. It allows for complex agentic workflows, state management, and human-in-the-loop interactions."
    plan = planner.plan(test_summary)
    print(plan)
