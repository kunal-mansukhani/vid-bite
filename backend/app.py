import shutil
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import google.generativeai as genai
import subprocess
import tempfile
import os
from fastapi.responses import JSONResponse
import logging
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from constants import get_plan_prompt, get_code_prompt, get_error_fixing_prompt
import anthropic
from RAG import query

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)
# Configure the Gemini API
app.mount("/media", StaticFiles(directory="media"), name="media")

genai.configure(api_key='AIzaSyCmf5l6rdp6UPR29W15b-6AaVrvWrA3-wU')
claude = anthropic.Anthropic(api_key='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')

class TextInput(BaseModel):
    text: str
    style: Optional[str] = "default"
    use_claude: Optional[bool] = False

@app.post("/generate_video")
async def generate_video(input: TextInput):
    try:
        manim_code = generate_manim_code(input.text, input.style, True)
        video_path = render_manim_video(manim_code)

        video_url = f"http://localhost:8000/{video_path}"

        print(f"Video URL: {video_url}")
        return JSONResponse(content={"videoUrl": video_url})
    except Exception as e:
        print(f"Error in generate_video: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def generate_manim_code(text: str, style: str, use_claude: bool) -> str:
    # Use Gemini 1.5 Flash to generate the animation plan
    flash_model = genai.GenerativeModel('gemini-1.5-flash')

    plan_prompt = get_plan_prompt(text)

    plan_response = flash_model.generate_content(plan_prompt)
    animation_plan = plan_response.text.strip()

    print("Animation Plan:")
    print(animation_plan)

    if use_claude:
        code_prompt = get_code_prompt(text)
        message = claude.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=2000,
            temperature=1,
            system="You are an expert Manim programmer. Respond only with complete, executable Manim code.",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": code_prompt
                        }
                    ]
                }
            ]
        )
        manim_code = message.content[0].text.strip()
    else:
        pro_model = genai.GenerativeModel('gemini-1.5-pro')
        code_response = pro_model.generate_content(get_code_prompt(animation_plan))
        manim_code = code_response.text.strip()

    manim_code = manim_code.replace("```python", "").replace("```", "")

    print("\nManim Code:")
    print(manim_code)

    return manim_code

def render_manim_video(manim_code: str, max_attempts=4):
    pro_model = genai.GenerativeModel('gemini-1.5-pro')
    flash_model = genai.GenerativeModel('gemini-1.5-flash')
    attempt = 0
    
    while attempt < max_attempts:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(manim_code)
            temp_file_path = temp_file.name

        try:
            media_dir = Path("media")
            if media_dir.exists():
                shutil.rmtree(media_dir)

            result = subprocess.run(["manim", "-qm", temp_file_path], 
                                    check=True, 
                                    capture_output=True, 
                                    text=True)
            
            video_dir = Path("media") / "videos" / Path(temp_file_path).stem / "720p30"
            video_files = list(video_dir.glob("*.mp4"))
            print(f"Video files: {video_files}")
            if video_files:
                video_path = video_files[0]
                return video_path
            else:
                raise FileNotFoundError(f"Generated video file not found in {video_dir}")
            

        except subprocess.CalledProcessError as e:
            print(f"Error in Manim execution (attempt {attempt + 1}): {e}")
            print(f"Manim error output: {e.stderr}")
            
            if attempt < max_attempts - 1:
                fix_response = flash_model.generate_content(get_error_fixing_prompt(manim_code, e.stderr))
                
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
