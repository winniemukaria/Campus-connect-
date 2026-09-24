from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from passlib.context import CryptContext
import sqlite3

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
def root():
    return {"name":"CampusConnect API","status":"running","docs":"/docs","frontend_should_use": "https://campus-connect-sigma-nine.vercel.app"}

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
        raise HTTPException(status_code=400, detail="Email already exists - try login")
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
        raise HTTPException(status_code=401, detail="User not found")
    uid, name, email, hashed_pw, role = row
    if not pwd_context.verify(data.password, hashed_pw):
        raise HTTPException(status_code=401, detail="Wrong password")
    return {"access_token": f"token-{uid}", "token_type":"bearer", "user": {"id":uid,"name":name,"email":email,"role":role}}
