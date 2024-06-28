import logging

from fastapi import FastAPI
from pydantic_settings import BaseSettings

from src.api.v1 import router as v1_router

logging.basicConfig(level=logging.DEBUG)


class Settings(BaseSettings):
    openapi_url: str = "/openapi.json"


app = FastAPI(
    title="Francis Tech Test",
)

app.include_router(v1_router)
