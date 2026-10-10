
from fastapi import FastAPI

app = FastAPI(
    title="ClientFlow CRM API",
    description="Backend API for the ClientFlow customer relationship management system.",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to ClientFlow CRM!",
        "status": "running",
    }


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "application": "ClientFlow CRM API",
    }


@app.get("/api/v1/about")
def about():
    return {
        "name": "ClientFlow CRM",
        "description": "A customer relationship management application",
        "version": "0.1.0",
    }
