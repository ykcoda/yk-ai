from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st

from app.utils import ai_settings

llm = ChatOllama(model=ai_settings.OLLAMA_MODEL)

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a Agine Coach. Answer any question related to the agile process",
        ),
        ("human", "{input}"),
    ]
)

st.title("Agile Guide")

input = st.text_input("Enter any question: ")
# response = llm.invoke(
#     prompt_template.format(city=city, month=month, language=language, budget=budget)
# )

chain = prompt_template | llm

if input:
    response = chain.invoke({"input": input})
    st.write(response.content)
