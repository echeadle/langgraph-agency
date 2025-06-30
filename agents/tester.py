
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class Tester:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a testing agent. Your job is to take Python code and generate `pytest` test cases for it. Provide only the test code, no explanations or extra text."),
                ("user", "Python Code: {code}"),
            ]
        )
        self.chain = self.prompt | self.llm

    def test(self, code: str) -> str:
        message = self.chain.invoke({"code": code})
        return getattr(message, "content", str(message))

if __name__ == "__main__":
    tester = Tester()
    # This is a placeholder code for testing purposes
    test_code = """def add(a, b):
    return a + b"""
    test_output = tester.test(test_code)
    print(test_output)
