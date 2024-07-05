import subprocess
import tempfile
import os
import shutil
from pathlib import Path
from fastapi import HTTPException
import google.generativeai as genai
from backend.constants import get_error_fixing_prompt

def render_manim_video(manim_code: str, max_attempts=3):
    flash_model = genai.GenerativeModel('gemini-1.5-flash')
    attempt = 0
    while attempt < max_attempts:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(manim_code)
            temp_file_path = temp_file.name

        try:
            media_dir = Path("backend/media")
            if media_dir.exists():
                print(f"Removing existing media directory: {media_dir}")
                shutil.rmtree(media_dir)
            else:
                print(f"Media directory does not exist: {media_dir}")

            result = subprocess.run(["manim", "-qm", temp_file_path], 
                                    check=True, 
                                    capture_output=True, 
                                    text=True,
                                    cwd='backend')
            print(result.stdout)
            print(result.stderr)
            
            video_dir = Path("backend/media") / "videos" / Path(temp_file_path).stem / "720p30"
            video_files = list(video_dir.glob("*.mp4"))
            if video_files:
                video_path = video_files[0]
                return video_path
            else:
                raise FileNotFoundError(f"Generated video file not found in {video_dir}")

        except subprocess.CalledProcessError as e:
            if attempt < max_attempts - 1:
                print(e.stderr)
                fix_response = flash_model.generate_content(get_error_fixing_prompt(manim_code, e.stderr))
                corrected_code = fix_response.text.split("```python")[-1].split("```")[0].strip()
                manim_code = corrected_code
                print(f"Corrected code: {corrected_code}")
            else:
                raise HTTPException(status_code=500, detail="Failed to generate video after multiple attempts")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            os.unlink(temp_file_path)

        attempt += 1

    raise HTTPException(status_code=500, detail="Failed to generate video after maximum attempts")
