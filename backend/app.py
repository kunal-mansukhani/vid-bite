import shutil
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import google.generativeai as genai
import subprocess
import tempfile
import os
from fastapi.responses import StreamingResponse
import logging
from pathlib import Path

app = FastAPI()

# Configure the Gemini API
genai.configure(api_key='AIzaSyCmf5l6rdp6UPR29W15b-6AaVrvWrA3-wU')

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
        print(f"Error in generate_video: {str(e)}")  # Add this line for logging
        raise HTTPException(status_code=500, detail=str(e))

def generate_manim_code(text: str, style: str) -> str:
    # Use Gemini 1.5 Flash to generate both the plan and the code
    flash_model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Task: Create a 20-30 second animation to teach and visualize the following concept using Manim: {text}. Consider the {style} style in your animation.

    1. First, provide a clear and structured outline of the animation plan, showing it step by step.
    2. Then, write the complete Manim code to implement this plan in one scene.

    For the Manim code:
    - Include all necessary imports
    - Provide the full class definition
    - Name the class 'AnGen'
    - Ensure the code is complete and ready to run without any additional dependencies
    - Wrap the code in ```python and ``` tags
    - The code should run out-of-the-box with no additional modifications like adding external images

    Begin your response with the animation plan, followed by the Manim code.
    """

    response = flash_model.generate_content(prompt)
    full_response = response.text.strip()

    # Split the response into plan and code
    plan, code_section = full_response.split("```python")
    manim_code = code_section.split("```")[0].strip()

    print("Animation Plan:")
    print(plan)
    print("\nManim Code:")
    print(manim_code)

    return manim_code

def render_manim_video(manim_code: str, max_attempts=4):
    flash_model = genai.GenerativeModel('gemini-1.5-flash')
    attempt = 0
    
    while attempt < max_attempts:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(manim_code)
            temp_file_path = temp_file.name

        try:
            # Clear the media directory before rendering
            media_dir = Path("backend") / "media"
            if media_dir.exists():
                shutil.rmtree(media_dir)

            # Run Manim to generate the video
            result = subprocess.run(["manim", "-qh", temp_file_path], 
                                    check=True, 
                                    capture_output=True, 
                                    text=True)
            
            # Determine the scene name (assuming it's the class name 'AnGen')
            scene_name = "AnGen"
            
            # Construct the expected path for the video
            video_dir = Path("backend") / "media" / "videos" / Path(temp_file_path).stem / "1080p60"
            video_path = video_dir / f"{scene_name}.mp4"
            
            if not video_path.exists():
                # If not found, try to glob for any MP4 in the directory
                video_files = list(video_dir.glob("*.mp4"))
                if video_files:
                    video_path = video_files[0]
                else:
                    raise FileNotFoundError(f"Generated video file not found in {video_dir}")
            
            # Open the video file in binary mode and return the file object
            return open(str(video_path), "rb")

        except subprocess.CalledProcessError as e:
            print(f"Error in Manim execution (attempt {attempt + 1}): {e}")
            print(f"Manim error output: {e.stderr}")
            
            if attempt < max_attempts - 1:
                # Ask Gemini to analyze the error and suggest fixes
                analysis_prompt = f"""
                The following Manim code produced an error:

                Code:
                {manim_code}

                Error:
                {e.stderr}

                Please analyze the error and suggest potential fixes. Then, implement the most promising fix and provide the entire corrected code.
                """
                fix_response = flash_model.generate_content(analysis_prompt)
                
                # Extract the corrected code from the response
                corrected_code = fix_response.text.split("```python")[-1].split("```")[0].strip()
                
                manim_code = corrected_code
                print(f"Updated Manim code (attempt {attempt + 2}):\n{manim_code}")
            else:
                raise HTTPException(status_code=500, detail="Failed to generate video after multiple attempts")

        except Exception as e:
            print(f"Unexpected error (attempt {attempt + 1}): {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            os.unlink(temp_file_path)

        attempt += 1

    raise HTTPException(status_code=500, detail="Failed to generate video after maximum attempts")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
