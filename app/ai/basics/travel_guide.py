from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
import streamlit as st

from app.utils import ai_settings

client = ChatOllama(model=ai_settings.OLLAMA_MODEL)
st.write("🔥 NEW VERSION LOADED")
st.title("Travel Guide")


prompt_template = PromptTemplate(
    input_variables=["city", "month", "language", "budget"],
    template="""Welcome to the {city} travel guide!
If you're visiting in {month}, here's what you can do:
1. Must-visit attractions.
2. Local cuisine you must try.
3. Useful phrases in {language}.
4. Tips for traveling on a {budget} budget.
Enjoy your trip!""",
)

city = st.text_input("city")
month = st.text_input("month")
language = st.text_input("clanguagey")
budget = st.text_input("budget")

response = client.invoke(
    prompt_template.format(city=city, month=month, language=language, budget=budget)
)

st.write(response.content)
