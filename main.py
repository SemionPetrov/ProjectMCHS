from fastapi import FastAPI

from src.frontend.frontend_main import frontend_app
from src.backend.backend_main import backend_app


main_app = FastAPI()

# Mount frontend and backend applications
main_app.mount("/", app=frontend_app, name="frontend")
main_app.mount("/api", app=backend_app, name="backend")
