from fastapi import FastAPI
from app.api.controller import exchange_rate_controller
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ['http://localhost:3000', 'https://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router in the main app
app.include_router(exchange_rate_controller.router)
