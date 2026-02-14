from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
import streamlit as st
import json
from app.utils import ai_settings


llm_openai = ChatOpenAI(
    api_key=ai_settings.OPENAI_API_KEY, model=ai_settings.OPENAI_MODEL
)

st.title("Ticket Generator")


class Ticket(BaseModel):
    date: str = Field(description="Show date")
    time: str = Field(description="Show time")
    theater: str = Field(description="Theater name")
    count: int = Field(description="Show number of tickets")
    movie: str = Field(description="Preffered movie")


pydantic_parser = PydanticOutputParser(pydantic_object=Ticket)

prompt = PromptTemplate(
    template="""
    Book us two tickets for this friday at 6:00pm. Choose any theater it does not matter. Send a confirmation email. our preferred movie is {query}.
    
    Format instructions:
    {format_instructions}
    """,
    input_variables=["query"],
    partial_variables={
        "format_instructions": pydantic_parser.get_format_instructions()
    },
)


query = st.text_input("Enter your prefered movie: ")


if query:
    output = (
        llm_openai.invoke(
            input=prompt.format(
                query=query,
            )
        )
    ).content
    st.write(type(output))
