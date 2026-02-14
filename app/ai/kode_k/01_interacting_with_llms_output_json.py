from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import streamlit as st
import json
from app.utils import ai_settings


llm_openai = ChatOpenAI(
    api_key=ai_settings.OPENAI_API_KEY, model=ai_settings.OPENAI_MODEL
)

output_parser = JsonOutputParser()

prompt = PromptTemplate(
    template="""list 4 contries in a {continent} and their capitals.
     
    Your response should be a json object eg. 
    {{
        "country":"string",
        "capital": "string"
    }}""",
    input_variables=["continent"],
)

output = (
    llm_openai.invoke(
        input=prompt.format(
            continent="Africa",
        )
    )
).content

print(output_parser.parse(output))
