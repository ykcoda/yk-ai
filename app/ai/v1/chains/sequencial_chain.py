from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate
import streamlit as st

from app.utils import ai_settings

llm = ChatOpenAI(model=ai_settings.OPENAI_MODEL, api_key=ai_settings.OPENAI_API_KEY)


title_prompt = PromptTemplate(
    input_variables=["topic"],
    template="""You are an experienced speech writer.
You need to craft an impactful title for a speech
on the following topic: {topic}
Answer exactly with one title.""",
)

speech_prompt = PromptTemplate(
    input_variables=["title", "emotion"],
    template="""
You need to write a powerful {emotion} speech of approximately 350 words
for the following title: {title}

Return ONLY valid JSON.
Do NOT include any explanation, markdown, or extra text.

The JSON must have exactly these keys:
- "title"
- "speech"
- "emotion"

Example format:
{{
  "title": "string",
  "speech": "string",
  "emotion": "string"
}}
""",
)


first_chain = (
    title_prompt | llm | StrOutputParser() | (lambda title: (st.write(title), title)[1])
)
second_chain = speech_prompt | llm | JsonOutputParser()
final_chain = (
    first_chain | (lambda title: {"title": title, "emotion": emotion}) | second_chain  # type: ignore
)

st.title("Speech Generator")
topic = st.text_input("Enter the topic:")
emotion = st.text_input("Enter the emotion:")

if topic and emotion:
    response = final_chain.invoke({"topic": topic})
    st.write(response)
