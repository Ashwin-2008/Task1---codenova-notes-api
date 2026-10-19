# Notes REST API

A RESTful API for creating, retrieving, updating, and deleting notes.

## Features

- Create, list, retrieve, update, and delete notes.
- SQLite persistent storage.
- Input validation.
- Consistent JSON error responses.
- Appropriate HTTP status codes.
- Interactive API documentation.
- Automated tests.

## Tech Stack

- Python
- FastAPI
- SQLite
- Pydantic
- Pytest

## Setup

Create a virtual environment:

    python -m venv .venv

Activate it on Windows:

    .venv\Scripts\Activate.ps1

Install dependencies:

    python -m pip install -r requirements.txt

Start the application:

    python -m uvicorn app.main:app --reload

## API Documentation

Once the server is running, open:

- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI specification: http://127.0.0.1:8000/openapi.json

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /notes | List notes |
| GET | /notes/{id} | Retrieve a note |
| POST | /notes | Create a note |
| PUT | /notes/{id} | Update a note |
| DELETE | /notes/{id} | Delete a note |

## Example Request

POST /notes

    {
      "title": "My first note",
      "content": "This is my note."
    }

Successful creation returns HTTP 201 Created.

## Run Tests

    python -m pytest -v

## Error Handling

The API returns consistent JSON errors for invalid input,
malformed JSON, missing resources, and unexpected server errors.
