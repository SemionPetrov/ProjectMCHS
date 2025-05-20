from http.client import HTTPException
from typing import Union, Dict

from fastapi import FastAPI
from pydantic import BaseModel


description = """
API для системы документооборота МЧС
"""

tags_metadata = [
    {
        "name": "тест",
        "description": "ничего не делают",

    },
]


app = FastAPI(
    title="ProjectMCHS",
    description=description,
    summary="API",
    version="0.0.1",
    openapi_tags=tags_metadata
)

@app.get("/", tags=["test"])
def get_all_terms():
    return "hello world!" 
