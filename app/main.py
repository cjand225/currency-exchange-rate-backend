from fastapi import FastAPI
from app.api.exchange import router as exchange_router

app = FastAPI()

# Include the API router in the main app
app.include_router(exchange_router)
