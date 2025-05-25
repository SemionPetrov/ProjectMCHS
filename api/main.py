import mysql.connector
from fastapi import FastAPI
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str = "mysql"
    DB_USER: str = "root"
    DB_PASSWORD: str = "pwd123admin"
    DB_PORT: int = 3306

settings = Settings()

app = FastAPI()
db = None

@app.on_event("startup")
async def startup_event():
    global db
    db = mysql.connector.connect(
        host=settings.DB_HOST,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        port=settings.DB_PORT
    )

@app.on_event("shutdown")
async def shutdown_event():
    global db
    if db:
        db.close()


@app.get("/", tags=["test"])
def get_root():
    return "Hello World!"


@app.get("/dbtest")
def test_database_connection():
    return {"status": "connected", "connection_id": id(db)}


@app.post("/dbtest")
def execute_query(query: str):
    try:

        cursor = db.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return {
            "status": "success",
            "results": result
        }
    except Exception as e:
        return e
