import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv(Path(__file__).parents[1] / ".env")
llm = ChatOpenAI(model="gpt-4o-mini")
print(llm.invoke("Xin chào?").content)
