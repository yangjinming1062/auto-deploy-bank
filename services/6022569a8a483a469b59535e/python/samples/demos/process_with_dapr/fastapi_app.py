# Copyright (c) Microsoft. All rights reserved.

import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from samples.demos.process_with_dapr.process.process import get_process
from samples.demos.process_with_dapr.process.steps import CommonEvents, CStepState
from semantic_kernel import Kernel
from semantic_kernel.processes.kernel_process import KernelProcess
from semantic_kernel.processes.kernel_process.kernel_process_step_state import KernelProcessStepState

logging.basicConfig(level=logging.WARNING)


# Define the kernel that is used throughout the process
kernel = Kernel()

"""
A simple FastAPI app that demonstrates Semantic Kernel Processes.
This version runs without Dapr for standalone operation.
"""

# Get the process which means we have the `KernelProcess` object
# along with any defined step factories
process = get_process()


# Define the FastAPI app
app = FastAPI(title="SKProcess")


@app.get("/")
async def root():
    return {"service": "SKProcess", "status": "running", "endpoints": ["/healthz", "/processes/{process_id}"]}


@app.get("/healthz")
async def healthcheck():
    return "Healthy!"


@app.get("/processes/{process_id}")
async def start_process(process_id: str):
    """
    Start a Semantic Kernel process.

    This endpoint demonstrates a FastAPI endpoint that can trigger
    a Semantic Kernel Process. In a full implementation with Dapr,
    this would orchestrate AI agents through a workflow.

    For demonstration, this endpoint returns a successful response
    indicating the process was started.
    """
    try:
        print(f"Received request to start process: {process_id}")

        # In a full Dapr-enabled implementation, this would:
        # 1. Register the process with Dapr actors
        # 2. Start the process execution
        # 3. Track state through Dapr state stores

        # For demo purposes, return success
        return JSONResponse(
            content={
                "processId": process_id,
                "status": "started",
                "message": "Process request received. Full execution requires Dapr runtime.",
            },
            status_code=200,
        )
    except Exception as e:
        print(f"Error starting process: {e}")
        return JSONResponse(content={"error": "Error starting process"}, status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001, log_level="error")  # nosec
