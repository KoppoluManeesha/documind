from fastapi import FastAPI
from routers import documents

# Create the FastAPI application
app = FastAPI(
    title="DocuMind",
    description="AI powered document assistant",
    version="0.1.0"
)

# Connect your routers — like Django's include() in urls.py
app.include_router(documents.router)

# Health check route
@app.get("/")
async def home():
    return {
        "message": "DocuMind is alive",
        "version": "0.1.0",
        "docs": "Visit /docs to see all API endpoints"
    }