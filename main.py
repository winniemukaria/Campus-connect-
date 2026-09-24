from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from passlib.context import CryptContext
import sqlite3
import os

app = FastAPI()
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

@app.get("/")
def root():
    return {"name":"CampusConnect API","status":"running"}

@app.post("/auth/register")
def register(data: Register):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    try:
        hashed = pwd_context.hash(data.password)
        cur.execute("INSERT INTO users (name,email,password,role) VALUES (?,?,?,?)", (data.name, data.email, hashed, data.role))
        con.commit()
        user_id = cur.lastrowid
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already exists")
    finally:
        con.close()
    return {"access_token": f"token-{user_id}", "token_type":"bearer", "user": {"id":user_id,"name":data.name,"email":data.email,"role":data.role}}

@app.post("/auth/login")
def login(data: dict):
    return {"access_token":"test-token","token_type":"bearer"}
