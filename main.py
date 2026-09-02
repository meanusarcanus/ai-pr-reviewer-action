#!/usr/bin/env python3
"""
GitHub Action Runner for PR-Agent Pro
Reads PR event data, analyzes git diff, audits security, and posts comments to GitHub PR.
"""

import os
import sys
import json
import requests
from pathlib import Path

from core.diff_parser import parse_unified_diff
from core.security_auditor import audit_diff_security
from core.pr_reviewer import review_code_diff
from core.changelog_generator import generate_pr_summary_and_changelog

def get_pr_diff(repo: str, pr_number: int, token: str) -> str:
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3.diff",
        "User-Agent": "PR-Agent-Pro"
    }
    res = requests.get(url, headers=headers, timeout=15)
    if res.status_code == 200:
        return res.text
    return ""

def post_pr_review(repo: str, pr_number: int, token: str, body: str, event: str = "COMMENT"):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/reviews"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "PR-Agent-Pro"
    }
    payload = {
        "body": body,
        "event": event
    }
    requests.post(url, headers=headers, json=payload, timeout=15)

def main():
    token = os.environ.get("GITHUB_TOKEN")
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    repo = os.environ.get("GITHUB_REPOSITORY")

    if not token or not event_path or not os.path.exists(event_path):
        print("⚠️ Not running in GitHub Actions environment or missing GITHUB_TOKEN.")
        print("Running in Standalone CLI Mode...")
        return

    with open(event_path) as f:
        event_data = json.load(f)

    pr_data = event_data.get("pull_request")
    if not pr_data:
        print("Not a pull_request event. Exiting.")
        return

    pr_number = pr_data.get("number")
    pr_title = pr_data.get("title", "Pull Request")

    print(f"🚀 Running PR-Agent Pro Review on PR #{pr_number}: '{pr_title}' in {repo}...")

    diff_text = get_pr_diff(repo, pr_number, token)
    if not diff_text:
        print("Could not fetch PR diff.")
        return

    # Run AI Review & Security Audit
    security_report = audit_diff_security(diff_text)
    review_report = review_code_diff(diff_text)
    changelog = generate_pr_summary_and_changelog(diff_text, pr_title=pr_title)

    # Build markdown review body
    body_parts = [
        changelog["summary_markdown"],
        f"\n### 🛡️ Security Audit: Grade {security_report['security_grade']} (Score: {security_report['security_score']}/100)\n"
    ]

    if security_report["findings"]:
        body_parts.append("#### ⚠️ Security Findings:")
        for f in security_report["findings"]:
            body_parts.append(f"- **{f['type']} ({f['severity']})**: {f['description']}\n  `{f['line_snippet']}`\n  *Fix*: {f['recommendation']}")
    else:
        body_parts.append("✅ **Zero security vulnerabilities or secret leaks detected.**\n")

    body_parts.append("### 📝 Code Review & Actionable Suggestions\n")
    for c in review_report["comments"]:
        body_parts.append(f"#### {c['file']}\n{c['comment']}\n")
        if c.get("suggestion"):
            body_parts.append(f"{c['suggestion']}\n")

    full_body = "\n".join(body_parts)
    verdict = "REQUEST_CHANGES" if security_report["status"] == "FAILED" else "COMMENT"

    post_pr_review(repo, pr_number, token, full_body, event=verdict)
    print("✅ PR-Agent Pro Review successfully posted to GitHub!")

if __name__ == "__main__":
    main()
