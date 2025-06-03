from fastapi import FastAPI

from database.db_connector import Base, engine
from routes import test_routes, user_routes 

app = FastAPI()

# init db
Base.metadata.create_all(bind=engine)

# add routes
app.include_router(test_routes.router)
app.include_router(user_routes.router)

# add fixtures to db

from database.fixtures.admin_fixture import setup_admin_fixture
setup_admin_fixture()
