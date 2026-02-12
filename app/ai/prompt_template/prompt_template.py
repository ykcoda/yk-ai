import streamlit as st
from app.ai.llm_connector import llm_connector


st.title("Cuisine Info")

country = st.text_input("Enter the country:")
no_of_paraghaphs = st.number_input("Enter the # of paragraphs", step=1)
language = st.text_input("Enter the language")

if country:
    response = llm_connector.promptTemplate(country, no_of_paraghaphs, language)
    st.write(response)
