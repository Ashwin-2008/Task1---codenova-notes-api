from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


def error_response(
    status_code: int,
    message: str,
    details: list | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": {
                "code": status_code,
                "message": message,
                "details": details or [],
            },
        },
    )


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_handler(
        request: Request,
        exc: RequestValidationError,
    ):
        details = [
            {
                "field": ".".join(str(part) for part in error["loc"]),
                "message": error["msg"],
            }
            for error in exc.errors()
        ]

        return error_response(400, "Invalid request", details)

    @app.exception_handler(StarletteHTTPException)
    async def http_handler(
        request: Request,
        exc: StarletteHTTPException,
    ):
        messages = {
            400: "Bad request",
            404: "Note not found",
            405: "Method not allowed",
        }

        return error_response(
            exc.status_code,
            messages.get(exc.status_code, str(exc.detail)),
        )

    @app.exception_handler(Exception)
    async def unexpected_handler(
        request: Request,
        exc: Exception,
    ):
        return error_response(500, "Internal server error")