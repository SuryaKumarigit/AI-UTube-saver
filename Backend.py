from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import yt_dlp

# Define FastAPI app
app = FastAPI()

# Allow CORS for all origins (for development purposes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a model for the response
class Result(BaseModel):
    message: str

# Define the download_video endpoint
@app.post("/download", response_model=Result)
def download_video(video_url: str = Form(...), save_path: str = Form(default="downloads")):
    # Ensure the save_path exists
    os.makedirs(save_path, exist_ok=True)

    # Configure yt_dlp options
    ydl_opts = {
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),  # Save with title as filename
    }

    try:
        # Use yt_dlp to download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return {"message": "Download complete!"}
    except Exception as e:
        return {"message": f"An error occurred: {e}"}
