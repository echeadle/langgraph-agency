
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
