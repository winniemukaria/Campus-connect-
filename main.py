
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sqlite3, json, os

from fastapi import FastAPI, HTTPException, Depends, Header, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from passlib.context import CryptContext
import jwt

BASE = Path(__file__).resolve().parent
DB = Path("/tmp/campusconnect.db")
UPLOADS = Path("/tmp/uploads")
UPLOADS.mkdir(exist_ok=True, parents=True)

SECRET_KEY = os.getenv("CAMPUS_CONNECT_SECRET", "CHANGE_THIS_SECRET_BEFORE_DEPLOYMENT_CHANGE_ME_12345")
ALGORITHM = "HS256"
TOKEN_DAYS = 7

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def conn():
    con = sqlite3.connect(DB, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    c = conn()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        created_at TEXT
    )""")
    c.commit()
    c.close()

init_db()

SECRET_KEY = os.getenv("CAMPUSCONNECT_SECRET", "CHANGE_THIS_SECRET_BEFORE_DEPLOYMENT")
ALGORITHM = "HS256"
TOKEN_DAYS = 7
pwd = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

app = FastAPI(title="CampusConnect API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this to your real domain before production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    c = conn()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('student','employer','admin')),
        university TEXT,
        course TEXT,
        year_of_study INTEGER,
        skills TEXT DEFAULT '',
        interests TEXT DEFAULT '',
        location TEXT,
        bio TEXT DEFAULT '',
        cv_filename TEXT,
        photo_filename TEXT,
        verified INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS opportunities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employer_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        description TEXT NOT NULL,
        opportunity_type TEXT NOT NULL,
        course TEXT,
        skills TEXT DEFAULT '',
        location TEXT,
        deadline TEXT,
        verified INTEGER DEFAULT 0,
        created_at TEXT NOT NULL,
        FOREIGN KEY(employer_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS saved_opportunities (
        user_id INTEGER NOT NULL,
        opportunity_id INTEGER NOT NULL,
        PRIMARY KEY(user_id, opportunity_id),
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(opportunity_id) REFERENCES opportunities(id)
    );

    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        opportunity_id INTEGER NOT NULL,
        status TEXT DEFAULT 'Applied',
        created_at TEXT NOT NULL,
        UNIQUE(student_id, opportunity_id),
        FOREIGN KEY(student_id) REFERENCES users(id),
        FOREIGN KEY(opportunity_id) REFERENCES opportunities(id)
    );

    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        read INTEGER DEFAULT 0,
        created_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reporter_id INTEGER NOT NULL,
        opportunity_id INTEGER NOT NULL,
        reason TEXT NOT NULL,
        status TEXT DEFAULT 'Open',
        created_at TEXT NOT NULL,
        FOREIGN KEY(reporter_id) REFERENCES users(id),
        FOREIGN KEY(opportunity_id) REFERENCES opportunities(id)
    );
    """)
    c.commit()
    c.close()

init_db()

def now():
    return datetime.now(timezone.utc).isoformat()

def make_token(user_id, role):
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(days=TOKEN_DAYS)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def current_user(authorization: str = Header(default="")):
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing Bearer token")
    token = authorization.split(" ", 1)[1]
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(data["sub"])
    except Exception:
        raise HTTPException(401, "Invalid or expired token")
    c = conn()
    user = c.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    c.close()
    if not user:
        raise HTTPException(401, "User not found")
    return dict(user)

def require_role(*roles):
    def dep(user=Depends(current_user)):
        if user["role"] not in roles:
            raise HTTPException(403, "You do not have permission for this action")
        return user
    return dep

class RegisterIn(BaseModel):
    name: str
    email: str
    password: str = Field(min_length=8)
    role: str = "student"
    university: str | None = None
    course: str | None = None
    year_of_study: int | None = None
    skills: str = ""
    interests: str = ""
    location: str | None = None
    bio: str = ""

class LoginIn(BaseModel):
    email: str
    password: str

class ProfileIn(BaseModel):
    name: str | None = None
    university: str | None = None
    course: str | None = None
    year_of_study: int | None = None
    skills: str | None = None
    interests: str | None = None
    location: str | None = None
    bio: str | None = None

class OpportunityIn(BaseModel):
    title: str
    company: str
    description: str
    opportunity_type: str
    course: str = ""
    skills: str = ""
    location: str = ""
    deadline: str | None = None

class ReportIn(BaseModel):
    reason: str

@app.get("/")
def root():
    return {"name":"CampusConnect API","status":"running","docs":"/docs"}

@app.get("/health")
def health():
    return {"status":"ok","database":DB.name}

@app.post("/auth/register")
def register(data: RegisterIn):
    role = data.role if data.role in ("student","employer") else "student"
    c = conn()
    try:
        cur = c.execute("""
            INSERT INTO users
            (name,email,password_hash,role,university,course,year_of_study,skills,interests,location,bio,created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, (data.name, data.email.lower().strip(), pwd.hash(data.password), role,
              data.university, data.course, data.year_of_study, data.skills, data.interests,
              data.location, data.bio, now()))
        c.commit()
        user_id = cur.lastrowid
    except sqlite3.IntegrityError:
        c.close()
        raise HTTPException(409, "Email is already registered")
    c.close()
    return {"token": make_token(user_id, role), "user": {"id":user_id,"name":data.name,"email":data.email,"role":role}}

@app.post("/auth/login")
def login(data: LoginIn):
    c = conn()
    u = c.execute("SELECT * FROM users WHERE email=?", (data.email.lower().strip(),)).fetchone()
    c.close()
    if not u or not pwd.verify(data.password, u["password_hash"]):
        raise HTTPException(401, "Invalid email or password")
    return {"token":make_token(u["id"],u["role"]),
            "user":{"id":u["id"],"name":u["name"],"email":u["email"],"role":u["role"]}}

@app.get("/me")
def me(user=Depends(current_user)):
    user.pop("password_hash", None)
    return user

@app.put("/me")
def update_me(data: ProfileIn, user=Depends(current_user)):
    fields = data.model_dump(exclude_none=True)
    if not fields:
        return user
    allowed = {"name","university","course","year_of_study","skills","interests","location","bio"}
    fields = {k:v for k,v in fields.items() if k in allowed}
    c = conn()
    sets = ", ".join(f"{k}=?" for k in fields)
    c.execute(f"UPDATE users SET {sets} WHERE id=?", (*fields.values(), user["id"]))
    c.commit()
    u = c.execute("SELECT * FROM users WHERE id=?", (user["id"],)).fetchone()
    c.close()
    return dict(u)

@app.post("/me/cv")
async def upload_cv(file: UploadFile = File(...), user=Depends(require_role("student"))):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".pdf",".doc",".docx"}:
        raise HTTPException(400, "Upload a PDF, DOC or DOCX CV")
    safe = f"user_{user['id']}_cv{suffix}"
    content = await file.read()
    if len(content) > 5_000_000:
        raise HTTPException(400, "CV must be 5 MB or smaller")
    (UPLOADS / safe).write_bytes(content)
    c=conn()
    c.execute("UPDATE users SET cv_filename=? WHERE id=?", (safe,user["id"]))
    c.commit(); c.close()
    return {"message":"CV uploaded","filename":safe}

@app.post("/opportunities")
def create_opportunity(data: OpportunityIn, user=Depends(require_role("employer"))):
    c=conn()
    cur=c.execute("""
      INSERT INTO opportunities
      (employer_id,title,company,description,opportunity_type,course,skills,location,deadline,created_at)
      VALUES (?,?,?,?,?,?,?,?,?,?)
    """,(user["id"],data.title,data.company,data.description,data.opportunity_type,data.course,
        data.skills,data.location,data.deadline,now()))
    c.commit(); oid=cur.lastrowid
    # Notify students whose course is similar.
    students=c.execute("SELECT id,course FROM users WHERE role='student'").fetchall()
    for s in students:
        if not data.course or not s["course"] or data.course.lower() in s["course"].lower() or s["course"].lower() in data.course.lower():
            c.execute("INSERT INTO notifications(user_id,title,message,created_at) VALUES(?,?,?,?)",
                      (s["id"],"New opportunity matching your profile",f"{data.title} at {data.company}",now()))
    c.commit(); c.close()
    return {"id":oid,"message":"Opportunity posted. It is pending verification."}

@app.get("/opportunities")
def list_opportunities(q: str="", course: str="", location: str="", opportunity_type: str=""):
    c=conn()
    rows=c.execute("""
      SELECT o.*, u.name AS employer_name, u.verified AS employer_verified
      FROM opportunities o JOIN users u ON u.id=o.employer_id
      WHERE (?='' OR lower(o.title||' '||o.description||' '||o.skills) LIKE lower('%'||?||'%'))
        AND (?='' OR lower(o.course) LIKE lower('%'||?||'%'))
        AND (?='' OR lower(o.location) LIKE lower('%'||?||'%'))
        AND (?='' OR o.opportunity_type=?)
      ORDER BY o.created_at DESC
    """,(q,q,course,course,location,location,opportunity_type,opportunity_type)).fetchall()
    c.close()
    return [dict(r) for r in rows]

@app.get("/opportunities/{oid}")
def get_opportunity(oid:int):
    c=conn()
    r=c.execute("""SELECT o.*,u.name employer_name,u.email employer_email,u.verified employer_verified
                   FROM opportunities o JOIN users u ON u.id=o.employer_id WHERE o.id=?""",(oid,)).fetchone()
    c.close()
    if not r: raise HTTPException(404,"Opportunity not found")
    return dict(r)

@app.post("/opportunities/{oid}/save")
def save_opportunity(oid:int,user=Depends(require_role("student"))):
    c=conn()
    if not c.execute("SELECT id FROM opportunities WHERE id=?",(oid,)).fetchone():
        c.close(); raise HTTPException(404,"Opportunity not found")
    c.execute("INSERT OR IGNORE INTO saved_opportunities(user_id,opportunity_id) VALUES(?,?)",(user["id"],oid))
    c.commit(); c.close()
    return {"saved":True}

@app.delete("/opportunities/{oid}/save")
def unsave_opportunity(oid:int,user=Depends(require_role("student"))):
    c=conn(); c.execute("DELETE FROM saved_opportunities WHERE user_id=? AND opportunity_id=?",(user["id"],oid)); c.commit(); c.close()
    return {"saved":False}

@app.get("/me/saved")
def saved(user=Depends(require_role("student"))):
    c=conn()
    rows=c.execute("""SELECT o.* FROM opportunities o JOIN saved_opportunities s ON s.opportunity_id=o.id
                     WHERE s.user_id=? ORDER BY o.created_at DESC""",(user["id"],)).fetchall()
    c.close(); return [dict(r) for r in rows]

@app.post("/opportunities/{oid}/apply")
def apply(oid:int,user=Depends(require_role("student"))):
    c=conn()
    if not c.execute("SELECT id FROM opportunities WHERE id=?",(oid,)).fetchone():
        c.close(); raise HTTPException(404,"Opportunity not found")
    try:
        cur=c.execute("INSERT INTO applications(student_id,opportunity_id,created_at) VALUES(?,?,?)",(user["id"],oid,now()))
        c.commit()
    except sqlite3.IntegrityError:
        c.close(); raise HTTPException(409,"You have already applied")
    c.execute("""INSERT INTO notifications(user_id,title,message,created_at)
                 SELECT employer_id,'New application received',? ,? FROM opportunities WHERE id=?""",
              (f"{user['name']} applied for opportunity #{oid}",now(),oid))
    c.commit(); c.close()
    return {"application_id":cur.lastrowid,"status":"Applied"}

@app.get("/me/applications")
def my_applications(user=Depends(require_role("student"))):
    c=conn()
    rows=c.execute("""SELECT a.*,o.title,o.company,o.deadline FROM applications a
                     JOIN opportunities o ON o.id=a.opportunity_id
                     WHERE a.student_id=? ORDER BY a.created_at DESC""",(user["id"],)).fetchall()
    c.close(); return [dict(r) for r in rows]

@app.get("/me/notifications")
def notifications(user=Depends(current_user)):
    c=conn()
    rows=c.execute("SELECT * FROM notifications WHERE user_id=? ORDER BY created_at DESC",(user["id"],)).fetchall()
    c.close(); return [dict(r) for r in rows]

@app.post("/notifications/{nid}/read")
def read_notification(nid:int,user=Depends(current_user)):
    c=conn(); c.execute("UPDATE notifications SET read=1 WHERE id=? AND user_id=?",(nid,user["id"])); c.commit(); c.close()
    return {"read":True}

@app.get("/me/matches")
def matches(user=Depends(require_role("student"))):
    c=conn()
    rows=c.execute("SELECT * FROM opportunities ORDER BY created_at DESC").fetchall()
    c.close()
    course=(user["course"] or "").lower()
    skills=set(x.strip().lower() for x in (user["skills"] or "").split(",") if x.strip())
    interests=set(x.strip().lower() for x in (user["interests"] or "").split(",") if x.strip())
    out=[]
    for r in rows:
        text=" ".join([(r["title"] or ""), (r["description"] or ""), (r["skills"] or ""), (r["course"] or "")]).lower()
        score=0
        if course and course in text: score += 45
        score += min(35, sum(1 for s in skills if s in text)*10)
        score += min(20, sum(1 for s in interests if s in text)*10)
        if score >= 20:
            d=dict(r); d["match_percent"]=min(score,99); out.append(d)
    out.sort(key=lambda x:x["match_percent"], reverse=True)
    return out[:30]

@app.post("/opportunities/{oid}/report")
def report(oid:int,data:ReportIn,user=Depends(current_user)):
    c=conn()
    if not c.execute("SELECT id FROM opportunities WHERE id=?",(oid,)).fetchone():
        c.close(); raise HTTPException(404,"Opportunity not found")
    c.execute("INSERT INTO reports(reporter_id,opportunity_id,reason,created_at) VALUES(?,?,?,?)",
              (user["id"],oid,data.reason,now()))
    c.commit(); c.close()
    return {"message":"Report submitted"}

@app.post("/admin/verify-employer/{uid}")
def verify_employer(uid:int,user=Depends(require_role("admin"))):
    c=conn(); c.execute("UPDATE users SET verified=1 WHERE id=? AND role='employer'",(uid,)); c.commit(); c.close()
    return {"verified":True}

@app.post("/admin/verify-opportunity/{oid}")
def verify_opportunity(oid:int,user=Depends(require_role("admin"))):
    c=conn(); c.execute("UPDATE opportunities SET verified=1 WHERE id=?",(oid,)); c.commit(); c.close()
    return {"verified":True}

@app.get("/admin/reports")
def admin_reports(user=Depends(require_role("admin"))):
    c=conn()
    rows=c.execute("""SELECT r.*,o.title,u.name reporter FROM reports r
                     JOIN opportunities o ON o.id=r.opportunity_id
                     JOIN users u ON u.id=r.reporter_id ORDER BY r.created_at DESC""").fetchall()
    c.close(); return [dict(r) for r in rows]
