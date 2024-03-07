import os
from dotenv import load_dotenv

from typing import Any, Dict

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    NAME: str = 'FastAPI Clean API'
    VERSION: str = '1.0'
    DESCRIPTION: str = 'FastAPI Clean REST API'

    SWAGGER_UI_PARAMETERS: Dict[str, Any] = {
        'displayRequestDuration': True,
        'filter': True,
    }

    DATABASE_URL: str = ""


settings = Settings()

load_dotenv('.env')
settings.DATABASE_URL = os.getenv("DATABASE_URL")
