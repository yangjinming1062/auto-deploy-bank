"""Simple FastAPI service demonstrating LangSmith SDK tracing."""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from langsmith import traceable

# LangSmith environment configuration
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "false").lower() == "true"
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "default")


@traceable(name="hello_world", run_type="chain")
def hello_world(name: str) -> dict:
    """Example traced function."""
    return {"message": f"Hello, {name}!", "project": LANGSMITH_PROJECT}


@traceable(name="calculate", run_type="tool")
def calculate(a: int, b: int, operation: str = "add") -> dict:
    """Example traced calculation function."""
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    else:
        result = a / b
    return {"result": result, "operation": operation}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context for startup/shutdown events."""
    print(f"LangSmith Tracing: {LANGSMITH_TRACING}")
    print(f"LangSmith Project: {LANGSMITH_PROJECT}")
    yield


app = FastAPI(
    title="LangSmith Demo API",
    description="Simple API demonstrating LangSmith SDK tracing",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"status": "ok", "message": "LangSmith Demo API is running"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/hello")
async def hello(name: str):
    """Traced hello endpoint."""
    return hello_world(name)


@app.post("/calc")
async def calc(a: int, b: int, operation: str = "add"):
    """Traced calculation endpoint."""
    return calculate(a, b, operation)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)