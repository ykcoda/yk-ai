from base64 import b64encode
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage

load_dotenv()


model = init_chat_model(model="gpt-5-nano")

# using url
# message = {
#     "role": "user",
#     "content": [
#         {"type": "text", "text": "Describe the content of this image"},
#         {
#             "type": "image",
#             "url": "https://images.pexels.com/photos/262897/pexels-photo-262897.jpeg",
#         },
#     ],
# }

# using base64
message = HumanMessage(
    content=[
        {"type": "text", "text": "Describe the content of this image"},
        {
            "type": "image",
            "base64": b64encode(open("food.jpg", "rb").read()).decode(),
            "mime_type": "image/jpeg",
        },
    ],
)

response = model.invoke([message])
print(response.content)
