from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from backend.models import TextInput
from backend.services.generate_manim_code import generate_manim_code
from backend.services.render_manim_video import render_manim_video
import boto3

router = APIRouter()
s3 = boto3.client('s3', 
                  aws_access_key_id="AKIA2UC3EIU4QANEQKGD",
                  aws_secret_access_key="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")

BUCKET_NAME = 'an-gen'

@router.post("/generate_video")
async def generate_video(input: TextInput):
    try:
        manim_code = generate_manim_code(input.text)
        video_path = render_manim_video(manim_code)
        s3_video_url = upload_video_to_s3(video_path)
        print(f"Video URL: {s3_video_url}")
        return JSONResponse(content={"videoUrl": s3_video_url})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    
def upload_video_to_s3(video_path: Path) -> str:
    try:
        s3.upload_file(str(video_path), BUCKET_NAME, video_path.name)
        s3_video_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{video_path.name}"
        return s3_video_url
    except Exception as e:
        print(f"Error uploading video to S3: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to upload video to S3")