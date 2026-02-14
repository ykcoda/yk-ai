from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import streamlit
from app.utils import ai_settings


llm_openai = ChatOpenAI(
    api_key=ai_settings.OPENAI_API_KEY, model=ai_settings.OPENAI_MODEL, streaming=True
)

streamlit.title("Programming Tutor")
subject = streamlit.text_input("Subject:")
concept = streamlit.text_input("Concept:")

sys_msg = "You are a {subject} teacher"
human_msg = "Tell me about {concept}"

prompt_message = ChatPromptTemplate.from_messages(
    [("system", sys_msg), ("human", human_msg)]
)

prompt = prompt_message.format(subject=subject, concept=concept)

response = llm_openai.invoke(prompt)
streamlit.write(response.content)
