from fastapi import Body, FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.api.routes.ai import ai
from app.ai.llm_connector import llm_connector

app = FastAPI()
app.include_router(ai)


@app.get("/", include_in_schema=False)
def root():
    return {"status": "system is up..."}


@app.post("/query")
def query(query: str = Body(...)):
    response = llm_connector.query(query)

    return {"Result": response}


@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}


@app.get("/scalar", include_in_schema=False)
def scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url)
