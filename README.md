# 🤖 PR-Agent Pro — Automated AI Pull Request Reviewer & Security Auditor

[![GitHub Action](https://img.shields.io/badge/GitHub_Action-PR--Reviewer-blue.svg)](https://github.com/marketplace)
[![MCP Protocol](https://img.shields.io/badge/MCP-Model_Context_Protocol-purple.svg)](https://modelcontextprotocol.io/)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Glama](https://img.shields.io/badge/Glama-MCP_Server-purple.svg)](https://glama.ai/mcp/servers)

An enterprise-grade **GitHub Action**, **Model Context Protocol (MCP) Server**, and CLI tool that automatically audits pull request code diffs, detects security flaws & secret leaks, posts inline 1-click suggested fixes, and generates semantic changelogs.

<p align="center">
  <img src="https://raw.githubusercontent.com/meanusarcanus/ai-pr-reviewer-action/master/assets/logo.jpg" alt="PR-Agent Pro Logo" width="200" style="border-radius: 24px; box-shadow: 0 8px 24px rgba(0,0,0,0.3);" />
</p>

---

## ⚡ Key Capabilities

* 🛡️ **Zero-Day Security & Secret Leak Scanner**: Scans modified lines for leaked Stripe/AWS/GitHub API keys, plaintext passwords, SQL injection vulnerabilities, and command injection risks.
* 📝 **Actionable 1-Click Code Review**: Posts inline GitHub review comments containing ````suggestion ```` code blocks that developers can apply directly from the GitHub UI with one click.
* 🤖 **Semantic PR Summary & Changelog**: Automatically synthesizes human-readable pull request overviews, risk scores, and release note bullets.
* 🔌 **Model Context Protocol (MCP) Server**: Equips **Claude Desktop, Cursor IDE, and Antigravity agents** to review local git diffs before pushing!

---

## 🚀 GitHub Action Quickstart (2 Minutes)

Add this workflow to your repository at `.github/workflows/ai-pr-reviewer.yml`:

```yaml
name: AI Pull Request Reviewer

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Run PR-Agent Pro Reviewer
        uses: meanusarcanus/ai-pr-reviewer-action@master
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          severity_threshold: "Medium"
```

---

## 🛠️ Model Context Protocol (MCP) Tools

| Tool Name | Parameters | Description |
| :--- | :--- | :--- |
| **`review_pr_diff`** | `diff_text` *(string, required)* | Reviews a git diff, analyzes code quality, and generates actionable comments with 1-click suggested diffs. |
| **`audit_code_security`** | `diff_text` *(string, required)* | Scans code changes for leaked secrets, SQL injection, and OWASP security flaws with a grade score (A+ to F). |
| **`generate_pr_changelog`** | `diff_text` *(string, required)*, `pr_title` *(string)* | Synthesizes a structured PR description and release notes from code changes. |

### Connect to Claude Desktop (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "ai-pr-reviewer": {
      "command": "python3",
      "args": ["/path/to/ai_pr_reviewer_action/mcp_server.py"]
    }
  }
}
```

---

## 📦 Python SDK & CLI Usage

```bash
pip install ai-pr-reviewer
```

```python
from ai_pr_reviewer import review_diff, audit_security, generate_changelog

diff = """
--- a/db.py
+++ b/db.py
@@ -10,3 +10,4 @@
+    query = f"SELECT * FROM users WHERE email = '{user_email}'"
+    cursor.execute(query)
"""

# Audit security
security = audit_security(diff)
print(f"Score: {security['security_score']}/100 | Grade: {security['security_grade']}")

# Run code review
review = review_code_diff(diff)
print(f"Verdict: {review['verdict']}")
```

---

## 📄 License
MIT License. Created by Meanus Arcanus.
