from starlette import status

from app.usecase.utils.responses import ResponseModel


HTTP_404_NOT_FOUND = {
    status.HTTP_404_NOT_FOUND: {
        "description": "Not Found",
        "model": ResponseModel,
    }
}


HTTP_409_CONFLICT = {
    status.HTTP_409_CONFLICT: {
        "description": "Some kind of conflict",
        "model": ResponseModel,
    }
}

HTTP_503_SERVICE_UNAVAILABLE = {
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
