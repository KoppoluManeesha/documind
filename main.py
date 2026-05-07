from fastapi import FastAPI
from routers import documents, auth

app = FastAPI(
    title="DocuMind",
    description="AI powered document assistant",
    version="0.1.0"
)

app.include_router(auth.router)
app.include_router(documents.router)

@app.get("/")
async def home():
    return {
        "message": "DocuMind is alive",
        "version": "0.1.0",
        "docs": "Visit /docs to see all API endpoints"
    }