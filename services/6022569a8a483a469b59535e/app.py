# Simple FastAPI app using Semantic Kernel without Dapr dependencies
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from semantic_kernel import Kernel

logging.basicConfig(level=logging.WARNING)

# Define the kernel that is used throughout the app
kernel = Kernel()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("## App startup ##")
    yield
    print("## App shutdown ##")


# Define the FastAPI app
app = FastAPI(title="SemanticKernel", lifespan=lifespan)


@app.get("/healthz")
async def healthcheck():
    return "Healthy!"


@app.get("/")
async def root():
    return {
        "service": "Semantic Kernel Python SDK",
        "status": "running",
        "endpoints": {
            "health": "/healthz",
            "processes": "/processes/{process_id}"
        }
    }


@app.get("/processes/{process_id}")
async def get_process_info(process_id: str):
    """Get information about a process (mock endpoint without Dapr)"""
    return JSONResponse(
        content={
            "processId": process_id,
            "status": "available",
            "message": "Dapr runtime not configured. This is a simplified endpoint."
        },
        status_code=200
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001, log_level="error")