from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Simple in-memory users (so login works) ---
users_db = {
    "winnie@test.com": {"email": "winnie@test.com", "password": "12345678", "name": "Winnie Mukaria", "role": "Founder"}
}

@app.get("/winnie.jpg")
async def winnie_photo():
    if os.path.exists("winnie.jpg"):
        return FileResponse("winnie.jpg")
    for f in os.listdir("."):
        if f.lower() == "winnie.jpg":
            return FileResponse(f)
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/Winnie.jpg")
async def winnie_cap():
    return await winnie_photo()

# --- LOGIN ENDPOINTS - FIXES Method Not Allowed ---
@app.post("/api/login")
@app.post("/login")
@app.post("/api/auth/login")
async def login(request: Request):
    try:
        data = await request.json()
        email = data.get("email", "").lower().strip()
        password = data.get("password", "")

        user = users_db.get(email)
        if user and user["password"] == password:
            return {"success": True, "user": user, "token": "founder-winnie-token", "message": "Welcome Founder!"}

        # Allow any email for demo if not found, create it
        if email and password:
            users_db[email] = {"email": email, "password": password, "name": email.split("@")[0], "role": "Student"}
            return {"success": True, "user": users_db[email], "token": "demo-token"}

        return JSONResponse({"success": False, "detail": "Invalid credentials"}, status_code=401)
    except Exception as e:
        return JSONResponse({"success": False, "detail": str(e)}, status_code=400)

@app.post("/api/register")
@app.post("/register")
@app.post("/api/auth/register")
async def register(request: Request):
    data = await request.json()
    email = data.get("email", "").lower().strip()
    users_db[email] = {"email": email, "password": data.get("password"), "name": data.get("name", email), "role": "Student"}
    return {"success": True, "user": users_db[email]}

@app.get("/api/health")
@app.get("/api")
async def health():
    return {"backend": "Connected", "users": len(users_db), "founder": "Winnie Mukaria"}

@app.get("/")
async def root():
    # Serve index.html if exists
    for name in ["index.html", "index_html"]:
        if os.path.exists(name):
            return FileResponse(name)
    # Find any html
    for f in os.listdir("."):
        if f.endswith(".html"):
            return FileResponse(f)
    return {"message": "CampusConnect LIVE", "photo": "/winnie.jpg", "founder": "Winnie Mukaria"}

# Mount static LAST
try:
    app.mount("/", StaticFiles(directory=".", html=True), name="static")
except:
    pass
