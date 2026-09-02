import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add root directory to sys.path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from core.security_auditor import audit_diff_security
from core.pr_reviewer import review_code_diff
from core.changelog_generator import generate_pr_summary_and_changelog

app = FastAPI(
    title="PR-Agent Pro — Automated AI PR Reviewer & Security Auditor API",
    description="Automated pull request code review, secret leak prevention, 1-click diff suggestions, and semantic changelogs.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

handler = app
application = app

# ==============================================================================
# Schemas
# ==============================================================================
class DiffReviewRequest(BaseModel):
    diff_text: str = Field(..., example="--- a/auth.py\n+++ b/auth.py\n@@ -10,3 +10,4 @@\n+    res = requests.get(url)\n")

class SecurityAuditRequest(BaseModel):
    diff_text: str = Field(..., example="--- a/config.py\n+++ b/config.py\n@@ -1,2 +1,3 @@\n+SECRET_KEY = 'secret_key_1234567890abcdef1234'\n")

class ChangelogRequest(BaseModel):
    diff_text: str = Field(..., example="--- a/api.py\n+++ b/api.py\n@@ -5,3 +5,6 @@\n+def new_endpoint(): pass\n")
    pr_title: Optional[str] = Field(default="Feature update")

# ==============================================================================
# Endpoints
# ==============================================================================
@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "service": "PR-Agent Pro — Automated AI PR Reviewer & Security Auditor API",
        "version": "1.0.0"
    }

@app.post("/api/v1/review-diff")
def review_diff_endpoint(payload: DiffReviewRequest):
    if not payload.diff_text.strip():
        raise HTTPException(status_code=400, detail="diff_text cannot be empty.")
    return review_code_diff(payload.diff_text)

@app.post("/api/v1/audit-security")
def audit_security_endpoint(payload: SecurityAuditRequest):
    if not payload.diff_text.strip():
        raise HTTPException(status_code=400, detail="diff_text cannot be empty.")
    return audit_diff_security(payload.diff_text)

@app.post("/api/v1/generate-changelog")
def generate_changelog_endpoint(payload: ChangelogRequest):
    if not payload.diff_text.strip():
        raise HTTPException(status_code=400, detail="diff_text cannot be empty.")
    title = payload.pr_title or "Feature update"
    return generate_pr_summary_and_changelog(payload.diff_text, pr_title=title)
