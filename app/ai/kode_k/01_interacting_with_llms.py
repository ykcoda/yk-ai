from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers.list import ListOutputParser
from langchain_core.output_parsers import CommaSeparatedListOutputParser
import streamlit as st

from app.utils import ai_settings


llm_openai = ChatOpenAI(
    api_key=ai_settings.OPENAI_API_KEY, model=ai_settings.OPENAI_MODEL
)

parser = CommaSeparatedListOutputParser()

prompt = PromptTemplate(
    template="list three {things}",
    input_variables=["things"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

output = prompt | llm_openai | parser

response = output.invoke({"things": "Countries that play soccer"})
print(response)
