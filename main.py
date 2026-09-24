from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from passlib.context import CryptContext
import sqlite3, os

app = FastAPI(title="CampusConnect API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
DB = "/tmp/campus.db"

def init_db():
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE, password TEXT, role TEXT)")
    con.commit()
    con.close()
init_db()

class Register(BaseModel):
    name: str
    email: str
    password: str
    role: str = "student"

class Login(BaseModel):
    email: str
    password: str

@app.get("/")
def serve_frontend():
    # If index.html exists, serve it as homepage
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    # fallback for campusconnect.html
    if os.path.exists("campusconnect.html"):
        return FileResponse("campusconnect.html")
    return {"name":"CampusConnect API","status":"running","docs":"/docs"}

@app.get("/campusconnect.html")
def serve_cc():
    if os.path.exists("campusconnect.html"):
        return FileResponse("campusconnect.html")
    return FileResponse("index.html") if os.path.exists("index.html") else {"error":"not found"}

@app.post("/auth/register")
def register(data: Register):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    try:
        hashed = pwd_context.hash(data.password)
        cur.execute("INSERT INTO users (name,email,password,role) VALUES (?,?,?,?)", (data.name, data.email, hashed, data.role))
        con.commit()
        uid = cur.lastrowid
    except sqlite3.IntegrityError:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Email already exists")
    finally:
        con.close()
    return {"access_token": f"token-{uid}", "token_type":"bearer", "user": {"id":uid,"name":data.name,"email":data.email,"role":data.role}}

@app.post("/auth/login")
def login(data: Login):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT id,name,email,password,role FROM users WHERE email=?", (data.email,))
    row = cur.fetchone()
    con.close()
    if not row:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="User not found")
    uid, name, email, hashed_pw, role = row
    if not pwd_context.verify(data.password, hashed_pw):
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Wrong password")
    return {"access_token": f"token-{uid}", "token_type":"bearer", "user": {"id":uid,"name":name,"email":email,"role":role}}

# Add dummy endpoints so your frontend's other pages don't break
@app.get("/opportunities")
def opps(): return []
@app.get("/matches")
def matches(): return []
