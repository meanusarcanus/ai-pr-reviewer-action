# 🤖 PR-Agent Pro — Automated AI PR Reviewer & Security Auditor API — Documentation

Welcome to the **PR-Agent Pro API**. Engineered for CI/CD pipelines, autonomous AI coding agents, and developer platforms to automate pull request code reviews, scan for security vulnerabilities & secret leaks, and generate semantic changelogs.

---

## ⚡ 1. Authentication & Headers

All requests to the RapidAPI endpoint require the standard RapidAPI authentication headers:

```http
x-rapidapi-key: YOUR_RAPIDAPI_KEY
x-rapidapi-host: ai-pr-reviewer.p.rapidapi.com
Content-Type: application/json
```

---

## 📝 2. Endpoint 1: Automated Code Review & 1-Click Suggestions (`POST /api/v1/review-diff`)

Analyzes a unified git diff and generates structured code review comments with 1-click suggested diff fixes.

### Request Body:
```json
{
  "diff_text": "diff --git a/auth.py b/auth.py\n--- a/auth.py\n+++ b/auth.py\n@@ -10,3 +10,4 @@\n+    res = requests.get(url)\n"
}
```

### Response Output:
```json
{
  "status": "success",
  "total_files_analyzed": 1,
  "total_additions": 1,
  "total_deletions": 0,
  "total_comments_generated": 1,
  "verdict": "REQUEST_CHANGES",
  "comments": [
    {
      "file": "auth.py",
      "type": "Robustness",
      "severity": "Medium",
      "comment": "⚠️ Network Call Without Explicit Error Handling: res = requests.get(url)",
      "suggestion": "```suggestion\n    try:\n        res = requests.get(url, timeout=10)\n    except requests.RequestException as e:\n        logger.error(f'Request failed: {e}')\n```"
    }
  ]
}
```

---

## 🛡️ 3. Endpoint 2: Security & Leaked Secret Audit (`POST /api/v1/audit-security`)

Scans modified code lines for leaked API secrets, SQL injections, and OWASP vulnerabilities with an A+ to F letter grade.

### Request Body:
```json
{
  "diff_text": "diff --git a/db.py b/db.py\n--- a/db.py\n+++ b/db.py\n@@ -1,2 +1,3 @@\n+cursor.execute(f'SELECT * FROM users WHERE id = {user_id}')\n"
}
```

### Response Output:
```json
{
  "status": "FAILED",
  "security_score": 25,
  "security_grade": "F",
  "total_issues_found": 1,
  "findings": [
    {
      "type": "Vulnerability",
      "severity": "HIGH",
      "description": "SQL Injection Vulnerability (String Interpolation in Query)",
      "line_snippet": "cursor.execute(f'SELECT * FROM users WHERE id = {user_id}')",
      "recommendation": "Use parameterized queries ($1, %s, or ORM) instead of f-strings."
    }
  ]
}
```

---

## 📚 4. Endpoint 3: Semantic PR Changelog Synthesizer (`POST /api/v1/generate-changelog`)

Synthesizes human-like pull request descriptions and release notes from code changes.

### Request Body:
```json
{
  "diff_text": "diff --git a/api.py b/api.py\n+++ b/api.py\n@@ -5,3 +5,6 @@\n+def get_user_profile(): pass\n",
  "pr_title": "Add user profile endpoint"
}
```
