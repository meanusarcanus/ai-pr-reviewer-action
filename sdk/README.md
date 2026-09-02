# 🤖 PR-Agent Pro Python SDK & CLI

Automated AI Pull Request Code Reviewer & Security Auditor.

---

## ⚡ Quickstart

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

# 1. Security & Secret Leak Audit
security = audit_security(diff)
print(f"Security Grade: {security['security_grade']} (Score: {security['security_score']}/100)")
for f in security['findings']:
    print(f"⚠️ {f['type']}: {f['description']}")

# 2. Automated Code Review with 1-Click Suggestions
review = review_code_diff(diff)
print(f"Verdict: {review['verdict']}")
for c in review['comments']:
    print(f"📝 {c['file']}: {c['comment']}")

# 3. Semantic Changelog
changelog = generate_pr_summary_and_changelog(diff, pr_title="Add user query")
print(changelog['summary_markdown'])
```
