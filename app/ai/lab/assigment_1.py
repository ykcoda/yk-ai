from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

import streamlit as st

from app.utils import ai_settings


client = ChatOpenAI(api_key=ai_settings.OPENAI_API_KEY, model=ai_settings.OPENAI_MODEL)

prompt_template = PromptTemplate(
    input_variables=["position", "company", "strengths", "weaknesses"],
    template="""You are a career coach. Provide tailored interview tips for the
position of {position} at {company}.
Highlight your strengths in {strengths} and prepare for questions
about your weaknesses such as {weaknesses}""",
)

st.title("Interview Helper")

position = st.text_input("position")
company = st.text_input("company")
strengths = st.text_area("strengths")
weaknesses = st.text_area("weaknesses")


response = client.invoke(
    prompt_template.format(
        position=position, company=company, strengths=strengths, weaknesses=weaknesses
    )
)

st.write(response.content)
