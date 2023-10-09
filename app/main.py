"""
main.py

This is the main entry point for the FastAPI application. It initializes the app instance and includes necessary routers.
"""

from app.api.controller import exchange_rate_controller
from app.factory import create_app

# Create a new FastAPI app instance using the factory function.
app = create_app()

# Include the API router in the main app.
app.include_router(exchange_rate_controller.router, prefix="/exchange-api/v1")
