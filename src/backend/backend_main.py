from fastapi import FastAPI

backend_app = FastAPI()

@backend_app.get("/")
def hello():
    return {"message": "Hello from API!"}
