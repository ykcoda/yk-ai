import streamlit as st
from app.ai.llm_connector import llm_connector


st.title("Ask Anything")

question = st.text_input("Enter the question:")

if question:
    response = llm_connector.query(question)
    st.write(response)
