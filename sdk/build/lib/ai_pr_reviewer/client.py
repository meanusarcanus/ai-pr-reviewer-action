import requests
from typing import Dict, Any, Optional

def review_diff(diff_text: str, base_url: str = "https://ai-pr-reviewer-api.vercel.app") -> Dict[str, Any]:
    endpoint = f"{base_url.rstrip('/')}/api/v1/review-diff"
    try:
        res = requests.post(endpoint, json={"diff_text": diff_text}, timeout=20)
        return res.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

def audit_security(diff_text: str, base_url: str = "https://ai-pr-reviewer-api.vercel.app") -> Dict[str, Any]:
    endpoint = f"{base_url.rstrip('/')}/api/v1/audit-security"
    try:
        res = requests.post(endpoint, json={"diff_text": diff_text}, timeout=20)
        return res.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

def generate_changelog(diff_text: str, pr_title: str = "Feature update", base_url: str = "https://ai-pr-reviewer-api.vercel.app") -> Dict[str, Any]:
    endpoint = f"{base_url.rstrip('/')}/api/v1/generate-changelog"
    try:
        res = requests.post(endpoint, json={"diff_text": diff_text, "pr_title": pr_title}, timeout=20)
        return res.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

class PRAgentClient:
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://ai-pr-reviewer-api.vercel.app"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def review(self, diff_text: str) -> Dict[str, Any]:
        return review_diff(diff_text, base_url=self.base_url)

    def audit(self, diff_text: str) -> Dict[str, Any]:
        return audit_security(diff_text, base_url=self.base_url)

    def changelog(self, diff_text: str, pr_title: str = "Feature update") -> Dict[str, Any]:
        return generate_changelog(diff_text, pr_title=pr_title, base_url=self.base_url)
