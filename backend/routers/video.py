from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from backend.models import TextInput
from backend.services.generate_manim_code import generate_manim_code
from backend.services.render_manim_video import render_manim_video

router = APIRouter()

@router.post("/generate_video")
async def generate_video(input: TextInput):
    try:
        manim_code = generate_manim_code(input.text, input.style, input.use_claude)
        video_path = render_manim_video(manim_code)
        video_url = f"http://localhost:8000/{str(video_path).replace('backend/', '', 1)}"

        return JSONResponse(content={"videoUrl": video_url})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    
# This is purely for RAG testing purposes
@router.post("/generate_code")
async def generate_code(input: TextInput):
    try:
        manim_code = generate_manim_code(input.text, input.style, True)
        return JSONResponse(content={"code": manim_code})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
