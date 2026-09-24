from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI(title="CampusConnect API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MEMORY STORAGE - works on Vercel!
USERS = {}
# Pre-add your account so login always works
USERS["winnie@test.com"] = {
    "id": 1,
    "email": "winnie@test.com",
    "password": "12345678",
    "full_name": "Winfred Mukami M'Mukaria",
    "university": "University of Embu",
    "course": "Bachelor of commerce",
    "year_of_study": 1,
    "skills": ["Accounting", "communication", "python", "tech"],
    "interests": ["Finance", "marketing"]
}

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    university: str
    course: str
    year_of_study: int
    skills: List[str] = []
    interests: List[str] = []

class UserLogin(BaseModel):
    email: str
    password: str

@app.get("/api/")
def root():
    return {"message": "CampusConnect API", "users": len(USERS)}

@app.post("/api/register")
def register(user: UserCreate):
    email = user.email.lower().strip()
    if email in USERS:
        raise HTTPException(status_code=400, detail="Email already exists")
    USERS[email] = user.dict()
    USERS[email]["id"] = len(USERS)
    return {"message": "Registered", "user": USERS[email]}

@app.post("/api/login")
def login(data: UserLogin):
    email = data.email.lower().strip()
    user = USERS.get(email)
    if not user or user["password"]!= data.password:
        raise HTTPException(status_code=401, detail="User not found or wrong password")
    return {"message": "Login successful", "user": user}

@app.get("/api/users/me")
def get_me(email: str):
    email = email.lower().strip()
    if email not in USERS:
        raise HTTPException(status_code=404, detail="Not found")
    return USERS[email]

# Serve frontend LAST
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
