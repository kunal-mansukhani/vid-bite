from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.routers import video
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

# Mount the static directory for media files
app.mount("/media", StaticFiles(directory="backend/media"), name="media")

# Include the video router
app.include_router(video.router, prefix="")
