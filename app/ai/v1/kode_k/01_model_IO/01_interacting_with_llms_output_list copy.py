from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import (
    CommaSeparatedListOutputParser,
    ListOutputParser,
)
import streamlit as st

from app.utils import ai_settings


llm_openai = ChatOpenAI(
    api_key=ai_settings.OPENAI_API_KEY, model=ai_settings.OPENAI_MODEL
)

output_parser = CommaSeparatedListOutputParser()

prompt = PromptTemplate(
    template="list three {things}\n Your response. should be in a comma seperated list eg. 'item1,item2,item3'",
    input_variables=["things"],
)

output = (
    llm_openai.invoke(
        input=prompt.format(
            things="Countries in africa that play football.",
        )
    )
).content

things = output_parser.parse(output.strip())
print(things[1])
