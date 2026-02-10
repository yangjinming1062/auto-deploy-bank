"""Simple FastAPI demo app demonstrating LangSmith SDK usage."""

import os
import time
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Import LangSmith SDK
import langsmith
from langsmith import traceable

app = FastAPI(
    title="LangSmith SDK Demo API",
    description="Demonstrates LangSmith Python SDK tracing capabilities",
    version="1.0.0",
)


class TraceRequest(BaseModel):
    """Request model for trace operations."""
    operation_name: str
    input_data: Optional[dict] = None
    tags: Optional[list[str]] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    langsmith_configured: bool


class TraceResponse(BaseModel):
    """Response for trace operations."""
    operation_name: str
    status: str
    run_id: str


# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check service health and LangSmith configuration."""
    return HealthResponse(
        status="healthy",
        langsmith_configured=bool(os.environ.get("LANGSMITH_API_KEY")),
    )


# Simple traced function
@traceable(name="demo_computation", tags=["demo", "computation"])
def demo_computation(input_value: int) -> dict:
    """A simple traced computation function."""
    time.sleep(0.1)  # Simulate work
    result = {"input": input_value, "output": input_value * 2}
    return result


@traceable(name="demo_chain", tags=["demo", "chain"])
def demo_chain(data: dict) -> dict:
    """A chained traced operation."""
    time.sleep(0.05)
    return {"processed": data}


# Main trace endpoint
@app.post("/trace", response_model=TraceResponse)
async def trace_operation(request: TraceRequest):
    """Execute a traced operation."""
    try:
        run_id = demo_computation(request.operation_name)
        return TraceResponse(
            operation_name=request.operation_name,
            status="completed",
            run_id=str(run_id),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Chain endpoint for more complex traces
@app.post("/chain")
async def chain_operations(data: dict):
    """Run a chain of traced operations."""
    step1 = demo_computation(len(str(data)))
    step2 = demo_chain(step1)
    return {"result": step2}


# Info endpoint
@app.get("/")
async def root():
    """Root endpoint with service info."""
    return {
        "service": "LangSmith SDK Demo API",
        "version": "1.0.0",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)