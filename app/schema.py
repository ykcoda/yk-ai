from sqlmodel import SQLModel


class ChatRequest(SQLModel):
    prompt: str


class ChatResponse(SQLModel):
    response: str
