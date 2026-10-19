from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import initialize_database
from app.errors import register_error_handlers
from app.routers.notes import router as notes_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="CodeNova Notes REST API",
    description="REST API for managing notes",
    version="1.0.0",
    lifespan=lifespan,
)

register_error_handlers(app)
app.include_router(notes_router)


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "success": True,
        "message": "Notes API is running",
    }