from fastapi import FastAPI

frontend_app = FastAPI()


@frontend_app.get("/")
def index():
    return "Hello from Frontend!"
