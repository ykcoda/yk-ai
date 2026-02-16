from ipywidgets import FileUpload  # type: ignore
from IPython.display import display
import base64
from langchain.messages import HumanMessage

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from lc.utils import ai_settings


uploader = FileUpload()
display(uploader)

uploaded_file = uploader.value[0]

content = uploaded_file["content"]

img_bytes = bytes(content)

img_base64 = base64.b64encode(img_bytes).decode("utf-8")


multimodel_question = HumanMessage(
    content=[
        {"type": "text", "text": "Tell me about this image"},
        {"type": "image", "base64": img_base64, "mime_type": "image/jpg"},
    ]
)


model = ChatOpenAI(api_key=ai_settings.OPENAI_API_KEY, model=ai_settings.OPENAI_MODEL)

agent = create_agent(model=model)

response = agent.invoke({"messages": [multimodel_question]})

print(response["messages"][-1].content)
