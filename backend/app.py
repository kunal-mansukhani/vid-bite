from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import google.generativeai as genai
import subprocess
import tempfile
import os
from fastapi.responses import StreamingResponse

app = FastAPI()

# Configure the Gemini API
genai.configure(api_key='YOUR_GEMINI_API_KEY')

class TextInput(BaseModel):
    text: str
    style: Optional[str] = "default"

@app.post("/generate_video")
async def generate_video(input: TextInput):
    try:
        # Generate Manim code using Gemini
        manim_code = generate_manim_code(input.text, input.style)
        
        # Render Manim video
        video_stream = render_manim_video(manim_code)
        
        # Stream video file
        return StreamingResponse(video_stream, media_type="video/mp4")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def generate_manim_code(text: str, style: str) -> str:
    # Use Gemini to generate Manim code
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Generate Manim code for the following text in {style} style:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text

def render_manim_video(manim_code: str):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        temp_file.write(manim_code)
        temp_file_path = temp_file.name

    try:
        # Run Manim to generate the video
        subprocess.run(["manim", "-qm", temp_file_path], check=True)
        
        # Assuming Manim generates a file named "Scene.mp4" in the same directory
        video_path = os.path.join(os.path.dirname(temp_file_path), "media/videos/Scene.mp4")
        
        if not os.path.exists(video_path):
            raise FileNotFoundError("Generated video file not found")
        
        # Open the video file in binary mode and return the file object
        return open(video_path, "rb")
    finally:
        os.unlink(temp_file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
