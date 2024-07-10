import subprocess
import tempfile
import os
import shutil
from pathlib import Path
from fastapi import HTTPException
import google.generativeai as genai
from backend.constants import get_error_fixing_prompt
from backend.RAG.RAG import RAG
import anthropic
claude = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def render_manim_video(manim_code: str, max_attempts=4):
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

            video_dir = Path("backend/media") / "videos" / Path(temp_file_path).stem / "720p30"
            video_files = list(video_dir.glob("*.mp4"))
            if video_files:
                video_path = video_files[0]
                return video_path
            else:
                raise FileNotFoundError(f"Generated video file not found in {video_dir}")

        except subprocess.CalledProcessError as e:
            if attempt < max_attempts - 1:
                error_lines = e.stderr.strip().split('\n')
                final_error = error_lines[-1] if error_lines else str(e)
                print(final_error)
                documentation_context = fetch_context(final_error)
                print(documentation_context)
                message = claude.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=2000,
                    temperature=1,
                    system="You are an expert Manim programmer and debugger. Before responding with the code, please make sure to think step by step and consider all the parameters and context. Then, respond with the complete, executable Manim code.",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": get_error_fixing_prompt(manim_code, e.stdout + '\n' + e.stderr) + f"\n\nAdditional documentation context that may be helpful: {documentation_context}"
                                }
                            ]
                    }
                ]
            )
                fix_response = message.content[0].text
                corrected_code = fix_response.split("```python")[-1].split("```")[0].strip()
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

def fetch_context(text: str, top_k: int = 5):
    rag = RAG(persist_dir="backend/RAG/knowledge_base")
    rag.load_vectorstore("backend/RAG/knowledge_base")
    context = rag.query(text, top_k)
    return context
