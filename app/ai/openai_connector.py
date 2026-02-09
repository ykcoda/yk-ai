from openai import OpenAI
from app.utils import ai_settings


class OpenaiConnector:
    def __init__(self):
        self.client = OpenAI(api_key=ai_settings.OPENAI_API_KEY)
