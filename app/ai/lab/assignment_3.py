import langchain_core.output_parsers
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser

import streamlit as st

from app.utils import ai_settings


llm_ollama = ChatOllama(model=ai_settings.OLLAMA_MODEL)
llm_openai = ChatOpenAI(
    api_key=ai_settings.OPENAI_API_KEY, model=ai_settings.OPENAI_MODEL  # type: ignore
)


subject_line_prompt = PromptTemplate(
    input_variables=["product_name", "features"],
    template="""You are an experienced marketing specialist.
Create a catchy subject line for a marketing
email promoting the following product: {product_name}.
Highlight these features: {features}.
Respond with only the subject line.""",
)


marketing_prompt = PromptTemplate(
    input_variables=["product_name", "subject_line", "target_audience"],
    template="""Write a marketing email of 300 words for the
product: {product_name}. Use the subject line:
{subject_line}. Tailor the message for the
following target audience: {target_audience}.
Format the output as a JSON object with three
keys: 'subject', 'audience', 'email' and fill
them with respective values.
reeturn the results as a json

using the below examples
{{
    "subject": "string",
    "audience" : "string",
    "email": "string"
}}
""",
)

first_chain = (
    subject_line_prompt
    | llm_ollama
    | StrOutputParser()
    | (lambda subject_line: (st.write(subject_line), subject_line)[1])
)

second_chain = marketing_prompt | llm_openai

final_chain = (
    first_chain
    | (
        lambda subject_line: {
            "subject_line": subject_line,
            "product_name": product_name,  # type: ignore
            "target_audience": target_audience,  # type: ignore
        }
    )
    | second_chain
    | JsonOutputParser()
)

st.title("Email Generator")
product_name = st.text_input("Product Name")
features = st.text_input("Features")
target_audience = st.text_input("Target Audience")


if product_name and features and target_audience:
    response = final_chain.invoke(
        {
            "product_name": product_name,
            "features": features,
            "target_audience": target_audience,
        }
    )
    st.write(response)
