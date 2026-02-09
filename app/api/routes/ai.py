from fastapi import APIRouter


ai = APIRouter(prefix="/api/v1/ai", tags=["ai"])


@ai.get("/")
def main():
    return {"status": "ai router is up"}
