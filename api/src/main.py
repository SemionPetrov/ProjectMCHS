from fastapi import FastAPI, APIRouter
from sqlalchemy import desc
from database.db_connector import Base, engine
from routes import admin_routes, user_routes, autentication_routes, attestation_management_routes, exercise_management_routes, personnnel_management_routes

description = """
Project MCHS API
"""


app = FastAPI(
        title="Project MCHS API",
        description=description,
        version="4.18",
        contact={"repo":"https://github.com/SemionPetrov/ProjectMCHS/tree/main"},
        )

# init db
Base.metadata.create_all(bind=engine)

api_router = APIRouter(
        prefix="/api",
)

# add routes
api_router.include_router(autentication_routes.router)
api_router.include_router(admin_routes.router)
api_router.include_router(user_routes.router)
api_router.include_router(attestation_management_routes.router)
api_router.include_router(exercise_management_routes.router)
api_router.include_router(personnnel_management_routes.router)


# prefix api with /api 
app.include_router(api_router)

# add privileges to db
from database.fixtures.privilege_fixtures import setup_privileges
setup_privileges()

# add fixtures to db
from database.fixtures.admin_fixture import setup_admin_fixture
setup_admin_fixture()

