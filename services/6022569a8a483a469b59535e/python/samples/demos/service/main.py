# Copyright (c) Microsoft. All rights reserved.

"""
Simple FastAPI service demonstrating Semantic Kernel functionality.
This service provides a basic chat interface using OpenAI or Azure OpenAI.
"""

import logging
import os
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion import OpenAIChatCompletion
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions.kernel_arguments import KernelArguments

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    message: str
    system_message: Optional[str] = None


class ChatResponse(BaseModel):
    response: str


# Global kernel and chat history
kernel = Kernel()
chat_history = ChatHistory()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the kernel with available AI service."""
    logger.info("Initializing Semantic Kernel...")

    # Try to initialize OpenAI service
    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    model_id = os.getenv("OPENAI_CHAT_MODEL_ID", "gpt-4o")

    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY", "")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    azure_deployment = os.getenv("AZURE_OPENAI_CHAT_MODEL_DEPLOYMENT_NAME", "")

    if azure_api_key and azure_endpoint:
        logger.info("Using Azure OpenAI service")
        kernel.add_service(
            OpenAIChatCompletion(
                service_id="azure",
                ai_model_id=azure_deployment or "gpt-4o",
                api_key=azure_api_key,
                endpoint=azure_endpoint,
                async_client=True,
            )
        )
    elif openai_api_key:
        logger.info(f"Using OpenAI service with model: {model_id}")
        kernel.add_service(
            OpenAIChatCompletion(
                service_id="openai",
                ai_model_id=model_id,
                api_key=openai_api_key,
                async_client=True,
            )
        )
    else:
        logger.warning("No API key found. Service will return mock responses.")

    yield


app = FastAPI(
    title="Semantic Kernel Service",
    description="A simple service demonstrating Semantic Kernel functionality",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "semantic-kernel"}


@app.get("/")
async def root():
    """Root endpoint with service information."""
    return {
        "service": "Semantic Kernel Python Service",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "chat": "/chat",
            "chat_history": "/chat/history",
        },
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat message and return a response.

    Args:
        request: ChatRequest containing the user's message

    Returns:
        ChatResponse with the assistant's reply
    """
    logger.info(f"Received message: {request.message}")

    # If no AI service is configured, return a mock response
    if not kernel.get_service("openai") and not kernel.get_service("azure"):
        return ChatResponse(
            response=f"Mock response to: {request.message}\n\n"
            f"Note: Configure OPENAI_API_KEY or AZURE_OPENAI_API_KEY to enable AI responses."
        )

    try:
        # Update system message if provided
        if request.system_message:
            chat_history.system_message = request.system_message

        # Add user message to history
        chat_history.add_user_message(request.message)

        # Create a simple chat function
        chat_function = kernel.add_function(
            plugin_name="ChatBot",
            function_name="Chat",
            prompt="{{$chat_history}}{{$user_input}}",
            template_format="semantic-kernel",
        )

        # Invoke the kernel
        result = await kernel.invoke(
            chat_function,
            KernelArguments(
                user_input=request.message,
                chat_history=str(chat_history),
            ),
        )

        # Add assistant response to history
        assistant_message = str(result)
        chat_history.add_assistant_message(assistant_message)

        logger.info(f"Generated response: {assistant_message[:100]}...")

        return ChatResponse(response=assistant_message)

    except Exception as e:
        logger.error(f"Error processing message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/chat/history")
async def get_chat_history():
    """Get the current chat history."""
    return {"chat_history": [msg.model_dump() for msg in chat_history.messages]}


@app.delete("/chat/history")
async def clear_chat_history():
    """Clear the chat history."""
    global chat_history
    chat_history = ChatHistory()
    return {"status": "chat history cleared"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "5001"))
    uvicorn.run(app, host="0.0.0.0", port=port)