"""FastAPI service for TiTok image generation.

This service exposes the TiTok model for image tokenization and generation via REST API.
"""

import io
import base64
import torch
import numpy as np
from PIL import Image
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager

# Global model instances - loaded lazily
tokenizer = None
generator = None
device = None
models_loaded = False
models_loading = False

LABEL_CACHE = None


def get_imagenet_labels():
    """Get ImageNet class labels."""
    global LABEL_CACHE
    if LABEL_CACHE is None:
        try:
            from imagenet_classes import imagenet_idx2classname
            LABEL_CACHE = imagenet_idx2classname
        except ImportError:
            LABEL_CACHE = {}
    return LABEL_CACHE


def load_models():
    """Load TiTok tokenizer and generator models."""
    global tokenizer, generator, device, models_loaded, models_loading

    if models_loaded:
        return

    # Prevent multiple threads from loading simultaneously
    if models_loading:
        return

    models_loading = True

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Loading models on device: {device}")

    try:
        # Load tokenizer from HuggingFace
        from modeling.titok import TiTok
        tokenizer = TiTok.from_pretrained("yucornetto/tokenizer_titok_l32_imagenet")
        tokenizer.eval()
        tokenizer.requires_grad_(False)
        tokenizer = tokenizer.to(device)

        # Load generator from HuggingFace
        from modeling.maskgit import ImageBert
        generator = ImageBert.from_pretrained("yucornetto/generator_titok_l32_imagenet")
        generator.eval()
        generator.requires_grad_(False)
        generator = generator.to(device)

        models_loaded = True
        print("Models loaded successfully")
    except Exception as e:
        print(f"Error loading models: {e}")
        models_loading = False
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI startup/shutdown."""
    # Don't load models at startup - use lazy loading
    yield


app = FastAPI(
    title="TiTok Image Generation API",
    description="Generate images using TiTok 1D Visual Tokenization",
    version="1.0.0",
    lifespan=lifespan
)


class GenerateRequest(BaseModel):
    """Request model for image generation."""
    label: int
    guidance_scale: float = 3.5
    randomize_temperature: float = 1.0
    num_sample_steps: int = 8


class GenerateResponse(BaseModel):
    """Response model for image generation."""
    image_base64: str
    label: int
    label_name: str


def image_to_base64(image: np.ndarray) -> str:
    """Convert numpy image to base64 string."""
    image_pil = Image.fromarray(image)
    buffer = io.BytesIO()
    image_pil.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "TiTok Image Generation API", "status": "running"}


@app.get("/health")
async def health_check():
    """Health check endpoint - returns healthy even if models not loaded yet."""
    return {"status": "healthy", "models_loaded": models_loaded}


@app.get("/status")
async def get_status():
    """Get detailed status including model loading state."""
    return {
        "status": "running",
        "models_loaded": models_loaded,
        "models_loading": models_loading,
        "device": "cuda" if torch.cuda.is_available() else "cpu"
    }


@app.get("/labels")
async def get_labels():
    """Get available ImageNet class labels."""
    labels = get_imagenet_labels()
    return {"labels": {str(k): v for k, v in labels.items()}}


@app.post("/generate", response_model=GenerateResponse)
async def generate_image(request: GenerateRequest):
    """Generate an image from a class label."""
    global models_loaded

    # Load models if not loaded yet
    if not models_loaded:
        load_models()

    if tokenizer is None or generator is None:
        raise HTTPException(status_code=503, detail="Models not loaded")

    try:
        from demo_util import sample_fn

        # Generate image
        generated_images = sample_fn(
            generator=generator,
            tokenizer=tokenizer,
            labels=[request.label],
            guidance_scale=request.guidance_scale,
            randomize_temperature=request.randomize_temperature,
            num_sample_steps=request.num_sample_steps,
            device=device
        )

        # Get the generated image
        generated_image = generated_images[0]

        # Get label name
        labels = get_imagenet_labels()
        label_name = labels.get(request.label, f"class_{request.label}")

        # Convert to base64
        image_base64 = image_to_base64(generated_image)

        return GenerateResponse(
            image_base64=image_base64,
            label=request.label,
            label_name=label_name
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)