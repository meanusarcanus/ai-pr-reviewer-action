"""
Automated Verification Suite for PR-Agent Pro
Tests git diff parsing, security leak auditing, 1-click suggestion generation, and FastAPI server.
"""

import sys
from pathlib import Path

# Add root directory to sys.path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from core.diff_parser import parse_unified_diff
from core.security_auditor import audit_diff_security
from core.pr_reviewer import review_code_diff
from core.changelog_generator import generate_pr_summary_and_changelog
from api.index import (
    app,
    DiffReviewRequest,
    review_diff_endpoint,
    SecurityAuditRequest,
    audit_security_endpoint,
    ChangelogRequest,
    generate_changelog_endpoint
)

SAMPLE_DIFF_CLEAN = """
diff --git a/services/user.py b/services/user.py
index e69de29..d95f3ad 100644
--- a/services/user.py
+++ b/services/user.py
@@ -1,3 +1,5 @@
+def get_user_profile(user_id: str) -> dict:
+    return {"id": user_id, "status": "active"}
"""

SAMPLE_DIFF_VULNERABLE = """
diff --git a/config.py b/config.py
--- a/config.py
+++ b/config.py
@@ -1,2 +1,3 @@
+API_KEY = "api_secret_1234567890abcdef1234"
+cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
+res = requests.get(url)
"""

def run_tests():
    print("=" * 65)
    print(" 🤖 TESTING PR-AGENT PRO (GITHUB ACTION & MCP REVIEWER)")
    print("=" * 65)

    # Test 1: Diff Parser
    print("\n[Test 1] Git Diff Parser & Chunk Extractor...")
    files = parse_unified_diff(SAMPLE_DIFF_CLEAN)
    assert len(files) == 1
    assert files[0]["filename"] == "services/user.py"
    assert files[0]["total_additions"] == 2
    print(f"✓ Parsed {len(files)} file: {files[0]['filename']} ({files[0]['total_additions']} additions)")

    # Test 2: Security & Leaked Secret Audit (Clean Diff)
    print("\n[Test 2] Security Audit on Clean Diff...")
    sec_clean = audit_diff_security(SAMPLE_DIFF_CLEAN)
    assert sec_clean["status"] == "PASSED"
    assert sec_clean["security_score"] == 100
    assert sec_clean["security_grade"] == "A+"
    print(f"✓ Security Score: {sec_clean['security_score']}/100 (Grade: {sec_clean['security_grade']}) - PASSED!")

    # Test 3: Security & Leaked Secret Audit (Vulnerable Diff)
    print("\n[Test 3] Security Audit on Vulnerable Diff...")
    sec_vuln = audit_diff_security(SAMPLE_DIFF_VULNERABLE)
    assert sec_vuln["status"] == "FAILED"
    assert sec_vuln["security_score"] <= 50
    assert len(sec_vuln["findings"]) >= 2
    print(f"✓ Detected {len(sec_vuln['findings'])} Critical/High Security Risks:")
    for f in sec_vuln["findings"]:
        print(f"  - [{f['severity']}] {f['type']}: {f['description']}")

    # Test 4: Code Review & 1-Click Suggestions
    print("\n[Test 4] Code Review & 1-Click Suggestion Generation...")
    review = review_code_diff(SAMPLE_DIFF_VULNERABLE)
    assert review["status"] == "success"
    assert review["total_comments_generated"] >= 1
    print(f"✓ Generated {review['total_comments_generated']} actionable code review comments:")
    for c in review["comments"]:
        print(f"  - {c['file']}: {c['type']} -> {c['severity']}")
        if c.get("suggestion"):
            print(f"    Suggested diff preview included!")

    # Test 5: Semantic Changelog & PR Summary Synthesizer
    print("\n[Test 5] Semantic Changelog & PR Summary Synthesizer...")
    changelog = generate_pr_summary_and_changelog(SAMPLE_DIFF_CLEAN, pr_title="Add user profile endpoint")
    assert changelog["status"] == "success"
    assert "PR-Agent Pro" in changelog["summary_markdown"]
    print(f"✓ Change Type: {changelog['change_type']}")
    print(f"✓ Suggested Title: {changelog['pr_title_suggestion']}")

    # Test 6: FastAPI Serverless Endpoints
    print("\n[Test 6] FastAPI Serverless Endpoints...")
    res_review = review_diff_endpoint(DiffReviewRequest(diff_text=SAMPLE_DIFF_CLEAN))
    assert res_review["status"] == "success"
    print("✓ POST /api/v1/review-diff: 200 OK")

    res_sec = audit_security_endpoint(SecurityAuditRequest(diff_text=SAMPLE_DIFF_CLEAN))
    assert res_sec["status"] == "PASSED"
    print("✓ POST /api/v1/audit-security: 200 OK")

    res_change = generate_changelog_endpoint(ChangelogRequest(diff_text=SAMPLE_DIFF_CLEAN, pr_title="Clean feature"))
    assert res_change["status"] == "success"
    print("✓ POST /api/v1/generate-changelog: 200 OK")

    print("\n" + "=" * 65)
    print(" 🎉 ALL PR-AGENT PRO TESTS PASSED 100% SUCCESSFULLY!")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    run_tests()
