import requests
from typing import Dict, Any, Optional

def review_diff(diff_text: str, rapidapi_key: Optional[str] = None, base_url: str = None) -> Dict[str, Any]:
    url = f"{base_url or 'https://ai-pr-reviewer.p.rapidapi.com'}/api/v1/review-diff"
    headers = {"Content-Type": "application/json"}
    if rapidapi_key:
        headers["x-rapidapi-key"] = rapidapi_key
        headers["x-rapidapi-host"] = "ai-pr-reviewer.p.rapidapi.com"
    try:
        res = requests.post(url, json={"diff_text": diff_text}, headers=headers, timeout=20)
        return res.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

def audit_security(diff_text: str, rapidapi_key: Optional[str] = None, base_url: str = None) -> Dict[str, Any]:
    url = f"{base_url or 'https://ai-pr-reviewer.p.rapidapi.com'}/api/v1/audit-security"
    headers = {"Content-Type": "application/json"}
    if rapidapi_key:
        headers["x-rapidapi-key"] = rapidapi_key
        headers["x-rapidapi-host"] = "ai-pr-reviewer.p.rapidapi.com"
    try:
        res = requests.post(url, json={"diff_text": diff_text}, headers=headers, timeout=20)
        return res.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

def generate_changelog(diff_text: str, pr_title: str = "Feature update", rapidapi_key: Optional[str] = None, base_url: str = None) -> Dict[str, Any]:
    url = f"{base_url or 'https://ai-pr-reviewer.p.rapidapi.com'}/api/v1/generate-changelog"
    headers = {"Content-Type": "application/json"}
    if rapidapi_key:
        headers["x-rapidapi-key"] = rapidapi_key
        headers["x-rapidapi-host"] = "ai-pr-reviewer.p.rapidapi.com"
    try:
        res = requests.post(url, json={"diff_text": diff_text, "pr_title": pr_title}, headers=headers, timeout=20)
        return res.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

class PRAgentClient:
    def __init__(self, rapidapi_key: Optional[str] = None, base_url: Optional[str] = None):
        self.rapidapi_key = rapidapi_key
        self.base_url = base_url or "https://ai-pr-reviewer.p.rapidapi.com"

    def review(self, diff_text: str) -> Dict[str, Any]:
        return review_diff(diff_text, rapidapi_key=self.rapidapi_key, base_url=self.base_url)

    def audit(self, diff_text: str) -> Dict[str, Any]:
        return audit_security(diff_text, rapidapi_key=self.rapidapi_key, base_url=self.base_url)

    def changelog(self, diff_text: str, pr_title: str = "Feature update") -> Dict[str, Any]:
        return generate_changelog(diff_text, pr_title=pr_title, rapidapi_key=self.rapidapi_key, base_url=self.base_url)

