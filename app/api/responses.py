from starlette import status

from models import ResponseModel

SERVICE_UNAVAILABLE = {
    status.HTTP_503_SERVICE_UNAVAILABLE: {
        "description": "Database error",
        "model": ResponseModel,
        "content": {
            "application/json": {
                "example": {"detail": "error", "message": "error description"}
            }
        }
    },
}