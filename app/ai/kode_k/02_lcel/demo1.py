from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.utils import ai_settings

import streamlit as st


# st.title("LCEL")

llm_openai = ChatOpenAI(
    api_key=ai_settings.OPENAI_API_KEY, model=ai_settings.OPENAI_MODEL
)

output_parser = StrOutputParser()

# prompt = ChatPromptTemplate.from_template(
#     """You are a helpful assitant. Answer the following question: {question}"""
# )

prompt = PromptTemplate(
    input_variables=["question"],
    template="""You are a helpful assitant. Answer the following question: {question}""",
)

chain = prompt | llm_openai | output_parser

chain.invoke({"question": "Tell me about The Godfather movie"})
