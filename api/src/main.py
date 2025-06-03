from fastapi import FastAPI
from fastapi.responses import FileResponse

from database.db_connector import Base, engine, get_db

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
    from database.db_connector import engine 


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
