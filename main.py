from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import instaloader
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

L = instaloader.Instaloader()

@app.get("/")
def home():
    return {"status": "Instaloader API is Live & Free!"}

@app.get("/get-reel")
def get_reel(url: str):
    match = re.search(r'/(?:reel|p|tv)/([A-Za-z0-9_-]+)', url)
    if not match:
        raise HTTPException(status_code=400, detail="Invalid Reel URL")
    
    shortcode = match.group(1)

    try:
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        if post.is_video:
            return {
                "success": True,
                "videoUrl": post.video_url,
                "title": post.caption[:60] if post.caption else "Instagram Reel"
            }
        raise HTTPException(status_code=400, detail="Yeh video nahi hai")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
