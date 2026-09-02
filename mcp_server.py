#!/usr/bin/env python3
"""
PR-Agent Pro — Model Context Protocol (MCP) Server
Provides standardized MCP tools for Claude Desktop, Cursor IDE, and Autonomous AI Coding Agents.
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any

# Add root directory to sys.path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from core.security_auditor import audit_diff_security
from core.pr_reviewer import review_code_diff
from core.changelog_generator import generate_pr_summary_and_changelog

TOOLS_DEFINITION = [
    {
        "name": "review_pr_diff",
        "description": "Reviews a git diff, analyzes code quality, performance, and generates actionable GitHub review comments with 1-click suggestion blocks.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "diff_text": {
                    "type": "string",
                    "description": "Unified git diff text or code snippet."
                }
            },
            "required": ["diff_text"]
        }
    },
    {
        "name": "audit_code_security",
        "description": "Audits a code diff or repository changes for leaked API keys/secrets, SQL injection, unsafe execution, and OWASP vulnerabilities.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "diff_text": {
                    "type": "string",
                    "description": "Git diff or code to scan for security flaws."
                }
            },
            "required": ["diff_text"]
        }
    },
    {
        "name": "generate_pr_changelog",
        "description": "Synthesizes human-readable PR descriptions, risk assessment, and release notes from a git diff.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "diff_text": {
                    "type": "string",
                    "description": "Unified git diff text."
                },
                "pr_title": {
                    "type": "string",
                    "description": "Optional title of the pull request.",
                    "default": "Feature update"
                }
            },
            "required": ["diff_text"]
        }
    }
]

def handle_call_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    diff = arguments.get("diff_text", "")

    if tool_name == "review_pr_diff":
        res = review_code_diff(diff)
        return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

    elif tool_name == "audit_code_security":
        res = audit_diff_security(diff)
        return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

    elif tool_name == "generate_pr_changelog":
        title = arguments.get("pr_title", "Feature update")
        res = generate_pr_summary_and_changelog(diff, pr_title=title)
        return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

    return {"content": [{"type": "text", "text": f"Unknown tool: {tool_name}"}]}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")

            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {
                            "name": "ai-pr-reviewer-mcp",
                            "version": "1.0.0"
                        }
                    }
                }
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()

            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": TOOLS_DEFINITION
                    }
                }
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()

            elif method == "tools/call":
                params = req.get("params", {})
                name = params.get("name")
                args = params.get("arguments", {})
                tool_res = handle_call_tool(name, args)
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": tool_res
                }
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()

        except Exception as e:
            sys.stderr.write(f"MCP Server Error: {str(e)}\n")

if __name__ == "__main__":
    main()
