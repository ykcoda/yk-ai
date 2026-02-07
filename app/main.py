from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from app.schema import ChatRequest, ChatResponse
from app.config import ai_settings
from app.ai.gemini import Gemini


app = FastAPI()


def load_system_prompt():
    try:
        with open("app/system_prompt.md") as f:
            return f.read()
    except FileNotFoundError:
        return None


system_prompt = load_system_prompt()
gemini_api_key = ai_settings.GOOGLE_API_KEY

ai_platform = Gemini(api_key=gemini_api_key, system_prompt=system_prompt)


@app.get("/")
def root():
    return {"Message": "API is running...."}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    response_text = ai_platform.chat(request.prompt)
    return ChatResponse(response=response_text)


@app.get("/scalar", include_in_schema=False)
def scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url)
