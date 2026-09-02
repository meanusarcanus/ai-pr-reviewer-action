"""
Security & Vulnerability Audit Engine
Scans code diffs for leaked secrets, SQL injection, unsafe exec/eval, and OWASP vulnerabilities.
"""

import re
from typing import List, Dict, Any

SECRET_PATTERNS = [
    (r"(?:api_secret|auth_token|secret_key)_[0-9a-zA-Z]{16,}", "Exposed API Secret Key (Critical)"),
    (r"(?:ghp|gho|ghu|ghs|ghr)_[0-9a-zA-Z]{36,}", "GitHub Personal Access Token (Critical)"),
    (r"AIza[0-9A-Za-z-_]{35}", "Google API Key (High)"),
    (r"AKIA[0-9A-Z]{16}", "AWS Access Key ID (Critical)"),
    (r"password\s*=\s*['\"][^'\"]+['\"]", "Hardcoded Plaintext Password (High)"),
    (r"SECRET_KEY\s*=\s*['\"][^'\"]+['\"]", "Hardcoded App Secret Key (High)")
]

VULNERABILITY_PATTERNS = [
    (r"(?:execute|cursor\.execute)\s*\(\s*f['\"].*\{.+\}", "SQL Injection Vulnerability (String Interpolation in Query)", "Use parameterized queries ($1, %s, or ORM) instead of f-strings."),
    (r"eval\s*\(", "Dangerous eval() Execution", "Avoid using eval() with untrusted user input; use ast.literal_eval() or JSON parser."),
    (r"exec\s*\(", "Dangerous exec() Execution", "Arbitrary code execution risk with exec()."),
    (r"subprocess\.Popen\s*\(.*shell\s*=\s*True", "Command Injection Risk (shell=True)", "Set shell=False and pass arguments as a list."),
    (r"dangerouslySetInnerHTML", "Potential Cross-Site Scripting (XSS)", "Sanitize HTML using DOMPurify before rendering.")
]

def audit_diff_security(diff_text: str) -> Dict[str, Any]:
    """
    Scans unified diff text for leaked secrets and security vulnerabilities.
    """
    findings = []
    lines = diff_text.splitlines()

    for idx, line in enumerate(lines, 1):
        # 1. Scan for leaked secrets
        for pattern, desc in SECRET_PATTERNS:
            if re.search(pattern, line):
                findings.append({
                    "type": "Leaked Secret",
                    "severity": "CRITICAL",
                    "description": desc,
                    "line_snippet": line.strip()[:80],
                    "recommendation": "Remove secret immediately, revoke key from provider dashboard, and use environment variables (.env)."
                })

        # 2. Scan for dangerous code vulnerabilities
        for pattern, title, fix in VULNERABILITY_PATTERNS:
            if re.search(pattern, line):
                findings.append({
                    "type": "Vulnerability",
                    "severity": "HIGH",
                    "description": title,
                    "line_snippet": line.strip()[:80],
                    "recommendation": fix
                })

    # Overall Security Grade Calculation
    if any(f["severity"] == "CRITICAL" for f in findings):
        status = "FAILED"
        grade = "F"
        score = 25
    elif len(findings) > 0:
        status = "WARNING"
        grade = "C"
        score = 65
    else:
        status = "PASSED"
        grade = "A+"
        score = 100

    return {
        "status": status,
        "security_score": score,
        "security_grade": grade,
        "total_issues_found": len(findings),
        "findings": findings
    }
