# CampusConnect — working backend

## What this backend provides
- Student and employer registration/login
- Secure password hashing
- JWT authentication
- Student profiles and CV upload
- Opportunity creation and search
- Course/skills/interests matching
- Saved opportunities
- Applications + application status
- Notifications
- Employer/opportunity verification endpoints
- Reporting suspicious opportunities
- Admin report review
- SQLite database for an easy first deployment

## Run locally

1. Install Python 3.11+.
2. Open a terminal in this folder.
3. Run:
   `python -m venv .venv`
4. Activate it:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`
5. Install:
   `pip install -r requirements.txt`
6. Set a strong secret before real deployment:
   - Windows PowerShell: `$env:CAMPUSCONNECT_SECRET="your-long-random-secret"`
   - macOS/Linux: `export CAMPUSCONNECT_SECRET="your-long-random-secret"`
7. Start:
   `uvicorn main:app --reload`
8. Open:
   `http://127.0.0.1:8000/docs`

The database file `campusconnect.db` is created automatically.

## Important before going public
This is a functional MVP backend, not a production security review. Before accepting real users:
- use a strong secret and HTTPS;
- restrict CORS to the real frontend domain;
- add email verification and password reset;
- add rate limiting and abuse protection;
- validate uploaded CVs and storage permissions;
- use managed PostgreSQL/object storage for scale;
- create a real admin account and verification workflow;
- connect the frontend to these API endpoints.
