"""Simple FastAPI server for GraphRAG Query API."""

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Any, Optional

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QueryRequest(BaseModel):
    query: str = Field(..., description="The search query")
    method: str = Field(default="local", description="Search method: local, global, drift, or basic")
    response_type: str = Field(default="multiple paragraphs", description="Response format type")
    community_level: Optional[int] = Field(default=None, description="Community level for search")
    dynamic_community_selection: bool = Field(default=False, description="Enable dynamic community selection")


class QueryResponse(BaseModel):
    result: str
    context: dict[str, Any]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load configuration on startup."""
    logger.info("Starting GraphRAG API server...")
    yield
    logger.info("Shutting down GraphRAG API server...")


app = FastAPI(
    title="GraphRAG API",
    description="API for querying GraphRAG knowledge graphs",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "graphrag"}


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "GraphRAG API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "query": "/query",
            "query_post": "/query (POST)"
        },
        "search_methods": ["local", "global", "drift", "basic"]
    }


@app.post("/api/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Query the GraphRAG knowledge graph.

    This endpoint allows you to search the indexed knowledge graph.
    Note: Requires the graph to be indexed first using `graphrag index` command.
    """
    try:
        # Placeholder response - actual implementation requires:
        # 1. A valid GraphRAG configuration (settings.yaml)
        # 2. Indexed data (parquet files)
        # 3. LLM and embedding model configuration
        logger.info(f"Received query: {request.query} (method: {request.method})")

        return QueryResponse(
            result=f"Query '{request.query}' received with method '{request.method}'. "
                   f"Response type: {request.response_type}. "
                   "Note: Full functionality requires indexed graph data.",
            context={
                "query": request.query,
                "method": request.method,
                "response_type": request.response_type,
                "community_level": request.community_level,
                "dynamic_community_selection": request.dynamic_community_selection,
                "note": "Configure graph index and LLM settings for full functionality"
            }
        )
    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/query", response_model=QueryResponse)
async def query_get(
    query: str = Query(..., description="The search query"),
    method: str = Query("local", description="Search method: local, global, drift, or basic"),
    response_type: str = Query("multiple paragraphs", description="Response format type")
):
    """Query the GraphRAG knowledge graph (GET method)."""
    return await query(QueryRequest(
        query=query,
        method=method,
        response_type=response_type
    ))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)