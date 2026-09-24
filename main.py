from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

USERS = {}
USERS["winnie@test.com"] = {
    "id": 1, "email": "winnie@test.com", "password": "12345678",
    "full_name": "Winfred Mukami", "university": "University of Embu",
    "course": "Bachelor of commerce", "year_of_study": 1,
    "skills": ["Accounting"], "interests": ["Finance"]
}

class UserCreate(BaseModel):
    email: str; password: str; full_name: str; university: str
    course: str; year_of_study: int; skills: List[str]=[]; interests: List[str]=[]

class UserLogin(BaseModel):
    email: str; password: str

@app.get("/api/")
def root(): return {"message": "API OK", "users": len(USERS)}

@app.post("/api/register")
def register(u: UserCreate):
    e=u.email.lower().strip()
    if e in USERS: raise HTTPException(400,"Email exists")
    USERS[e]=u.dict(); USERS[e]["id"]=len(USERS); return {"user": USERS[e]}

@app.post("/api/login")
def login(d: UserLogin):
    e=d.email.lower().strip()
    u=USERS.get(e)
    if not u or u["password"]!=d.password: raise HTTPException(401,"User not found")
    return {"user": u}

# Try to serve frontend, else return simple login page
@app.get("/", response_class=HTMLResponse)
def serve_home():
    for p in ["frontend/index.html", "./frontend/index.html", "index.html"]:
        if os.path.exists(p):
            with open(p) as f: return f.read()
    # Fallback HTML if frontend folder missing
    return """
    <html><body style="font-family:Arial;padding:20px;max-width:400px;margin:auto">
    <h1>CampusConnect</h1>
    <h3>Login (Test account: winnie@test.com / 12345678)</h3>
    <input id="email" placeholder="Email" value="winnie@test.com" style="width:100%;padding:10px;margin:5px 0"><br>
    <input id="pass" type="password" placeholder="Password" value="12345678" style="width:100%;padding:10px;margin:5px 0"><br>
    <button onclick="login()" style="width:100%;padding:10px;background:blue;color:white;border:none">Log in</button>
    <p id="msg"></p>
    <script>
    async function login(){
      const r=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:document.getElementById('email').value,password:document.getElementById('pass').value})});
      const j=await r.json();
      document.getElementById('msg').innerText = r.ok? 'SUCCESS! Welcome '+j.user.full_name : JSON.stringify(j);
    }
    </script></body></html>
    """
