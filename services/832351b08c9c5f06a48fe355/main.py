import os
import glob
import shutil
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from openai import OpenAI
from langchain_openai import ChatOpenAI
from templates import enhance_prompt, initial_dialogue_prompt, plan_prompt
from utils.script import generate_script, parse_script_plan
from utils.audio_gen import generate_podcast

# Load environment variables
load_dotenv()

# Initialize OpenAI clients
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

client = OpenAI(api_key=OPENAI_API_KEY)
llm = ChatOpenAI(model="gpt-4o-mini")

# Setup chains
chains = {
    "plan_script_chain": plan_prompt | llm | parse_script_plan,
    "initial_dialogue_chain": initial_dialogue_prompt | llm | StrOutputParser(),
    "enhance_chain": enhance_prompt | llm | StrOutputParser(),
}

app = FastAPI(title="Paper to Podcast API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Working directory for processing
WORK_DIR = "/tmp/podcast_work"
os.makedirs(WORK_DIR, exist_ok=True)

OUTPUT_DIR = "/tmp/podcast_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.get("/")
async def root():
    return {"message": "Paper to Podcast API - Upload a PDF to generate a podcast"}


@app.post("/generate")
async def generate_podcast_endpoint(file: UploadFile = File(...)):
    """
    Upload a PDF file and generate a podcast audio file.
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    # Save uploaded file
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    pdf_filename = f"input_{timestamp}.pdf"
    pdf_path = os.path.join(WORK_DIR, pdf_filename)

    try:
        content = await file.read()
        with open(pdf_path, "wb") as f:
            f.write(content)

        # Clean up old files
        for f in glob.glob(f"{WORK_DIR}/*.txt"):
            os.remove(f)
        for f in glob.glob(f"{OUTPUT_DIR}/*.mp3"):
            os.remove(f)

        # Generate the podcast
        print("Generating podcast script...")
        script = generate_script(pdf_path, chains, llm)
        print("Podcast script generation complete!")

        print("Generating podcast audio files...")
        generate_podcast(script, client)
        print("Podcast generation complete!")

        # Find the generated podcast file
        podcast_files = glob.glob(f"{OUTPUT_DIR}/podcast_*.mp3")
        if not podcast_files:
            raise HTTPException(status_code=500, detail="Failed to generate podcast")

        # Return the most recent podcast
        latest_podcast = max(podcast_files, key=os.path.getmtime)

        # Clean up working files
        os.remove(pdf_path)

        return FileResponse(
            path=latest_podcast,
            media_type="audio/mpeg",
            filename=f"podcast_{timestamp}.mp3"
        )

    except Exception as e:
        # Cleanup on error
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        raise HTTPException(status_code=500, detail=f"Error generating podcast: {str(e)}")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}