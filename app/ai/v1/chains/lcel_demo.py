from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
import streamlit as st

from app.utils import ai_settings

llm = ChatOllama(model=ai_settings.OLLAMA_MODEL)

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

st.write("🔥 LCEL_DEMO")
st.title("Travel Guide")

city = st.text_input("city")
month = st.text_input("month")
language = st.text_input("clanguagey")
budget = st.selectbox(label="budget", options=["", "low", "medium", "high"])

# response = llm.invoke(
#     prompt_template.format(city=city, month=month, language=language, budget=budget)
# )

chain = prompt_template | llm

if city and month and language and budget:
    response = chain.invoke(
        {
            "city": city,
            "month": month,
            "language": language,
            "budget": budget,
        }
    )

    st.write(response.content)
