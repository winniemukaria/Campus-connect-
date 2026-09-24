from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="CampusConnect - Founder Winnie Mukaria")

# Allow all frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- EXPLICIT PHOTO ROUTE - FIXES YOUR ISSUE ---
@app.get("/winnie.jpg")
async def serve_winnie():
    # Check root
    if os.path.exists("winnie.jpg"):
        return FileResponse("winnie.jpg")
    # Check lowercase search
    for file in os.listdir("."):
        if file.lower() == "winnie.jpg":
            return FileResponse(file)
    return {"detail": "Not Found - winnie.jpg missing"}

@app.get("/Winnie.jpg")
async def serve_winnie_cap():
    return await serve_winnie()

# --- SIMPLE API FOR FRONTEND ---
@app.get("/api")
async def api_root():
    return {"message": "CampusConnect API - Founder Winnie Mukaria - UoEm BCom", "status": "LIVE"}

@app.get("/api/health")
async def health():
    return {"backend": "Connected", "users": 1, "founder": "Winnie Mukaria"}

# --- SERVE FRONTEND ---
# Find which index file exists
def find_index():
    candidates = ["index.html", "index_html", "campusconnect.html", "index.htm"]
    for c in candidates:
        if os.path.exists(c):
            return c
    # Look for any html with CampusConnect
    for f in os.listdir("."):
        if f.endswith(".html") and "CampusConnect" in f:
            return f
    return None

@app.get("/")
async def root():
    index_file = find_index()
    if index_file and os.path.exists(index_file):
        return FileResponse(index_file)
    # Fallback
    return {"message": "CampusConnect is LIVE - Founder Winnie Mukaria", "photo": "/winnie.jpg"}

# --- IMPORTANT: Mount static files LAST so API routes work ---
# This serves all static files like winnie.jpg, logo etc
if os.path.exists("."):
    try:
        app.mount("/", StaticFiles(directory=".", html=True), name="static")
    except:
        pass
