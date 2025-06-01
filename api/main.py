from re import M
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic_settings import BaseSettings

import models
from database import Base, engine, get_db

# 
app = FastAPI()

# init db
Base.metadata.create_all(bind=engine)


@app.get("/dbtest")
def test_database_connection():
    db = get_db()
    return {"status": "connected", "connection": db}

@app.post("/dbtest")
def execute_query(query: str):
    from sqlalchemy import text
    from database import engine 


    with engine.connect() as connection:
        try:
            ready_query = text(query)
            result = connection.execute(ready_query)
            
            # Convert result rows to lists of strings
            rows = [[str(value) for value in row] for row in result.fetchall()]
            
            # Format the output as a string
            if not rows:
                formatted_output = "Query executed successfully, but returned no rows."
            else:
                formatted_output = " ".join([", ".join(row) for row in rows])
                
            return {
                "status": "success",
                "query": query,
                "results": formatted_output
            }
        except Exception as e:
            return {
                "status": "failure",
                "query": query,
                "error": str(e)
            } 

@app.get("/db/erdiagram")
def build_er_diagram():
    from eralchemy import render_er 
    from database import Base
    
    filename = 'db_er_diagram.png'
    render_er(Base, filename)
    
    return FileResponse(filename)


