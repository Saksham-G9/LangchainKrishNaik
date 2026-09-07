from fastapi import FastAPI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from langserve import add_routes

from dotenv import load_dotenv
import os
import uvicorn

os.environ["OPEN_API_KEY"] = os.getenv("OPEN_API_KEY", "")

load_dotenv()


llm = ChatOpenAI(model="gpt-4o-mini",)

parser = StrOutputParser()

# Prompt Template


generic_template = "Translate the following into {language}"

prompt_template = ChatPromptTemplate.from_messages(
    [("system", generic_template), ("user", "{text}")]
)

chain = prompt_template | llm | parser

# App definition

app = FastAPI(title="Langchain Server", version="1.0")

add_routes(app, chain, path="/chain")
if __name__ == "__main__":
    uvicorn.run(app)
