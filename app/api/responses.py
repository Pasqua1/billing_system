from starlette import status

from app.models import ResponseModel


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


NOT_FOUND = {
    status.HTTP_404_NOT_FOUND: {
        "description": "Not Found",
        "model": ResponseModel,
    }
}


CONFLICT = {
    status.HTTP_409_CONFLICT: {
        "description": "Some kind of conflict",
        "model": ResponseModel,
    }
}
