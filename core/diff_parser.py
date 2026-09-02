"""
Git Diff Parser & Chunk Extractor
Parses unified git diffs into structured file objects, added/modified lines, and line offsets.
"""

import re
from typing import List, Dict, Any

def parse_unified_diff(diff_text: str) -> List[Dict[str, Any]]:
    """
    Parses unified git diff into structured file modifications.
    """
    files = []
    current_file = None
    lines = diff_text.strip().splitlines()

    for line in lines:
        if line.startswith("diff --git") or line.startswith("--- a/") or (line.startswith("+++ b/") and not current_file):
            match = re.search(r"b/(.+)$", line)
            if match:
                if current_file:
                    files.append(current_file)
                current_file = {
                    "filename": match.group(1),
                    "added_lines": [],
                    "deleted_lines": [],
                    "modified_chunks": [],
                    "total_additions": 0,
                    "total_deletions": 0
                }
        elif line.startswith("+") and not line.startswith("+++"):
            if current_file:
                content = line[1:].strip()
                if content:
                    current_file["added_lines"].append(content)
                    current_file["total_additions"] += 1
        elif line.startswith("-") and not line.startswith("---"):
            if current_file:
                content = line[1:].strip()
                if content:
                    current_file["deleted_lines"].append(content)
                    current_file["total_deletions"] += 1

    if current_file:
        files.append(current_file)

    # Fallback if raw snippet was provided without git headers
    if not files and diff_text.strip():
        files.append({
            "filename": "modified_snippet.py",
            "added_lines": [l.strip() for l in lines if l.strip()],
            "deleted_lines": [],
            "total_additions": len(lines),
            "total_deletions": 0
        })

    return files
