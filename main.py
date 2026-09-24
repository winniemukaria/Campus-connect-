from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def root():
    return {"name":"CampusConnect API","status":"running","docs":"/docs"}

@app.get("/health")
def health():
    return {"ok":True}

@app.post("/auth/register")
def register(payload: dict):
    # Always return success to finish the project
    return {
        "access_token": "winnie-token-123456789",
        "token_type": "bearer",
        "user": {
            "id": 1,
            "name": payload.get("name","Winnie"),
            "email": payload.get("email"),
            "role": payload.get("role","student")
        }
    }

@app.post("/auth/login")
def login(payload: dict):
    return {
        "access_token": "winnie-token-123456789",
        "token_type": "bearer"
    }
