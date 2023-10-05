"""
config.py

This module manages the configuration settings for the application, primarily by reading environment variables.
"""

import os

# Fetch the environment type (e.g., production, development) from the environment variables.
ENV = os.getenv("FASTAPI_ENV")

# Check and raise an error if the essential environment variable isn't set.
if ENV is None:
    raise ValueError("The ENV environment variable is not set!")

# Set configuration values based on the environment type.
if ENV == "production":
    ORIGINS = []
elif ENV == "development":
    ORIGINS = ['http://localhost:3000', 'https://localhost:3000']
