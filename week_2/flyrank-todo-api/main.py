from fastapi import FastAPI

app = FastAPI(
    title="Task API",
    description="CRUD API for managing to-do tasks",
    version="1.0"
)

@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }