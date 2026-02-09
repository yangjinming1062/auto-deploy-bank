import torch
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import os

app = FastAPI(title="Qwen2 Fine-tuned Model Service")

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model and tokenizer
tokenizer = None
model = None
device = "cuda" if torch.cuda.is_available() else "cpu"

MODEL_LOADED = False


def load_model():
    global tokenizer, model, MODEL_LOADED
    if MODEL_LOADED:
        return

    print("Loading base model and tokenizer...")
    base_model_path = "./qwen/Qwen2-1___5B-Instruct/"

    # Check if base model exists, if not download from ModelScope
    if not os.path.exists(base_model_path):
        from modelscope import snapshot_download
        print("Downloading model from ModelScope...")
        snapshot_download("qwen/Qwen2-1.5B-Instruct", cache_dir="./", revision="master")
        base_model_path = "./qwen/Qwen2-1___5B-Instruct/"

    tokenizer = AutoTokenizer.from_pretrained(
        base_model_path, use_fast=False, trust_remote_code=True
    )

    torch_dtype = torch.bfloat16 if device == "cuda" else torch.float32
    model = AutoModelForCausalLM.from_pretrained(
        base_model_path, device_map="auto" if device == "cuda" else None,
        torch_dtype=torch_dtype
    )
    if device == "cpu":
        model = model.to(device)

    # Try to load LoRA adapter if it exists
    lora_path = "./output/Qwen2"
    if os.path.exists(lora_path):
        print("Loading LoRA adapter...")
        for root, dirs, files in os.walk(lora_path):
            if "adapter_model.bin" in files or "adapter_config.json" in files:
                model = PeftModel.from_pretrained(model, model_id=root)
                print(f"Loaded LoRA from {root}")
                break

    MODEL_LOADED = True
    print("Model loaded successfully!")


class PredictionRequest(BaseModel):
    instruction: str
    input_text: str


class PredictionResponse(BaseModel):
    instruction: str
    input_text: str
    output: str


@app.on_event("startup")
async def startup_event():
    load_model()


@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": MODEL_LOADED}


@app.get("/")
async def root():
    """Root endpoint with service info"""
    return {
        "service": "Qwen2 Fine-tuned Model Service",
        "version": "1.0.0",
        "endpoints": {
            "health": "GET /health",
            "predict": "POST /predict",
            "docs": "GET /docs",
            "openai_completions": "POST /v1/chat/completions"
        }
    }


@app.post("/v1/chat/completions")
async def chat_completions(request: dict):
    """OpenAI-compatible chat completions endpoint"""
    messages = request.get("messages", [])
    max_tokens = request.get("max_tokens", 512)

    # Convert messages to text format
    prompt = ""
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        prompt += f"{role}: {content}\n"

    text = tokenizer.apply_chat_template(
        [{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(device)

    generated_ids = model.generate(
        model_inputs.input_ids,
        max_new_tokens=max_tokens,
        do_sample=False
    )
    generated_ids = [
        output_ids[len(input_ids):]
        for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": response
                }
            }
        ],
        "usage": {
            "prompt_tokens": len(model_inputs.input_ids[0]),
            "completion_tokens": len(generated_ids[0])
        }
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    messages = [
        {"role": "system", "content": request.instruction},
        {"role": "user", "content": request.input_text}
    ]

    text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(device)

    generated_ids = model.generate(
        model_inputs.input_ids,
        max_new_tokens=512,
        do_sample=False
    )
    generated_ids = [
        output_ids[len(input_ids):]
        for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return PredictionResponse(
        instruction=request.instruction,
        input_text=request.input_text,
        output=response
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)