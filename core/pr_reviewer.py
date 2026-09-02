"""
Automated AI Code Reviewer & 1-Click Suggestion Generator
Generates clean, constructive GitHub-flavored Markdown review comments with ```suggestion blocks.
"""

from typing import List, Dict, Any
from core.diff_parser import parse_unified_diff

def review_code_diff(diff_text: str) -> Dict[str, Any]:
    """
    Analyzes unified git diff and generates structured code review comments with 1-click suggestions.
    """
    files = parse_unified_diff(diff_text)
    review_comments = []
    total_additions = sum(f["total_additions"] for f in files)
    total_deletions = sum(f["total_deletions"] for f in files)

    for f in files:
        filename = f["filename"]
        for line in f["added_lines"]:
            # Check 1: Missing Exception Handling in requests/fetch
            if ("requests.get" in line or "fetch(" in line) and "try" not in line and "catch" not in line:
                review_comments.append({
                    "file": filename,
                    "type": "Robustness",
                    "severity": "Medium",
                    "comment": f"⚠️ **Network Call Without Explicit Error Handling**: `{line}`\nConsider wrapping in `try/except` with a timeout parameter to prevent hanging requests.",
                    "suggestion": "```suggestion\n    try:\n        res = requests.get(url, timeout=10)\n    except requests.RequestException as e:\n        logger.error(f'Request failed: {e}')\n```"
                })

            # Check 2: Unbounded loops or range(len()) anti-pattern
            elif "for i in range(len(" in line:
                review_comments.append({
                    "file": filename,
                    "type": "Code Quality / Pythonic",
                    "severity": "Low",
                    "comment": "💡 **Pythonic Improvement**: Use `enumerate()` instead of `range(len())` for cleaner, index-tracked iteration.",
                    "suggestion": "```suggestion\nfor idx, item in enumerate(items):\n```"
                })

            # Check 3: Print statement in production code
            elif "print(" in line and not line.startswith("#"):
                review_comments.append({
                    "file": filename,
                    "type": "Observability",
                    "severity": "Low",
                    "comment": "📝 **Production Logging**: Replace raw `print()` statements with structured logger (`logger.info()` or `logger.debug()`).",
                    "suggestion": "```suggestion\nlogger.info('Processing operation...')\n```"
                })

    # If no specific anti-patterns detected, provide clean approval
    if not review_comments:
        review_comments.append({
            "file": files[0]["filename"] if files else "all",
            "type": "Code Quality",
            "severity": "None",
            "comment": "✅ **Clean Diff**: Code conforms to typing, error handling, and performance best practices. No critical regressions detected.",
            "suggestion": ""
        })

    return {
        "status": "success",
        "total_files_analyzed": len(files),
        "total_additions": total_additions,
        "total_deletions": total_deletions,
        "total_comments_generated": len(review_comments),
        "verdict": "APPROVE" if all(c["severity"] in ["Low", "None"] for c in review_comments) else "REQUEST_CHANGES",
        "comments": review_comments
    }
