import os
import argparse
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from rich import print as rprint
from rich.panel import Panel
from rich.rule import Rule
from rich.style import Style

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    temperature: float = 0.8
    max_len: int = 2048

class ChatResponse(BaseModel):
    response: str

class OnlineChat:
    def __init__(self, args):
        self.model_name = args.model
        self.temperature = args.temperature
        self.max_len = args.max_len
        self.history = []

        # Use transformers for CPU inference (simpler than vLLM)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(args.model)
        self.model = AutoModelForCausalLM.from_pretrained(
            args.model,
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True
        )
        self.model.to(self.device)

        self.hard_stop = ["<user>", "<AI>", "<system>"]

    def generate(self):
        prompt = self.conv_to_prompt()
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=self.max_len,
                temperature=self.temperature,
                do_sample=True,
                top_p=0.95,
                pad_token_id=self.tokenizer.eos_token_id
            )

        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        gen_seqs = generated_text[len(prompt):] if len(generated_text) > len(prompt) else generated_text

        for st in self.hard_stop:
            if st in gen_seqs:
                gen_seqs = gen_seqs.split(st)[0]

        return gen_seqs.strip()

    def conv_to_prompt(self):
        prompt = "<system>: You are an AI coding assistant that helps people with programming. Write a response that appropriately completes the user's request.\n"
        prefix = {
            "user": "<user>: {content}\n",
            "model": "<AI>: {content}\n"
        }
        for r, conv in self.history:
            prompt = prompt + prefix[r].format(content=conv)
        prompt = prompt + "<AI>: "
        return prompt

    def chat_one_turn(self, text):
        self.history.append(("user", text))
        try:
            res = self.generate()
        except Exception as e:
            self.history.pop()
            return f"Error: {str(e)}"
        self.history.append(("model", res))
        return res

    def clear_history(self):
        self.history = []


# Global chat instance
chat_instance = None

def get_chat_instance():
    global chat_instance
    if chat_instance is None:
        parser = argparse.ArgumentParser()
        parser.add_argument('--model', type=str, default='bigcode/starcoder', help="Model path or name")
        parser.add_argument('--temperature', type=float, default=0.8, help="Sampling temperature")
        parser.add_argument('--max_len', type=int, default=2048, help="Maximum generation length")
        args = parser.parse_args([])
        chat_instance = OnlineChat(args)
    return chat_instance


@app.get("/")
def read_root():
    return {"service": "Xwin-Coder Chat API", "status": "running"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    chat = get_chat_instance()
    response = chat.chat_one_turn(request.message)
    return ChatResponse(response=response)


@app.post("/clear")
def clear_chat():
    chat = get_chat_instance()
    chat.clear_history()
    return {"status": "cleared"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=40543)