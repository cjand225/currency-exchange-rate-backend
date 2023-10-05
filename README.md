# Currency Exchange Rate Web Application (Backend)

This repository contains the backend portion of the Currency Exchange Rate Web Application. The backend is implemented using FastAPI in Python and is responsible for fetching currency exchange rates from the Bank of Canada API.

## Features

- Fetch currency exchange rates based on user-specified parameters.
- Handle errors and validation for API requests.
- Dockerized for easy deployment and distribution.

## Prerequisites

- Python 3.11+
- Docker (optional, for containerization)
- An environment variable `ENV` set to either "production" or "development".

## Getting Started

Follow these steps to set up and run the backend of the Currency Exchange Rate Web Application:

1. **Clone the Repository**:

   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**:

   If not using Docker, create a virtual environment and install the required dependencies:

   ```
       python -m venv venv
       source venv/bin/activate
       pip install -r requirements.txt
   ```

3. **Run the Application**:

   Before running the application, ensure you have set the `ENV` environment variable.

   If not using Docker, you can run the application locally using Uvicorn:

   ```
       uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

   If using Docker, build and run the Docker container using the provided makefile:

   ```
       make up  # See the Makefile for more commands
   ```

   The API will be accessible at http://localhost:8000.

4. **API Documentation**:

   Access the Swagger documentation at http://localhost:8000/docs for API details and interactive testing.

5. **API Endpoints**:

   - `/exchange_rates/`: Fetch currency exchange rates based on user-specified parameters. See API documentation for details.
