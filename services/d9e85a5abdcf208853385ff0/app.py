from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from kwaiagents.agent_start import AgentService

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    id: str = "test"
    query: str
    history: list = []
    llm_name: str = "gpt-3.5-turbo"
    max_tokens_num: int = 4096
    lang: str = "en"
    tool_names: str = '["auto"]'
    max_iter_num: int = 1
    agent_name: str = ""
    agent_bio: str = ""
    agent_instructions: str = ""
    external_knowledge: str = ""


@app.post("/chat")
def chat(request: ChatRequest):
    agent_service = AgentService()
    result = agent_service.chat(request.dict())
    return result


@app.get("/chat")
def chat_get():
    return {
        "message": "Chat API - Use POST method",
        "example": {
            "url": "/chat",
            "method": "POST",
            "content-type": "application/json",
            "body": {
                "query": "your message",
                "id": "optional-id",
                "history": [],
                "llm_name": "gpt-3.5-turbo"
            }
        }
    }


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)