#!/usr/bin/env python3
"""
run_dom_tool_wrapper.py

Simple tool wrapper so the DOM/MCP system can call Python "tools" as subprocesses.

Usage examples:

  # Find Gemini CLI (used by mcp.general_agent.find_gemini_cli)
  python run_dom_tool_wrapper.py mcp.general_agent.find_gemini_cli

  # Run a Gemini CLI extensions command (optional extra tool)
  echo '{"subcommand": "list"}' | \
      python run_dom_tool_wrapper.py mcp.general_agent.run_gemini_extensions --payload -

The script:
  - Takes a tool name as the first positional argument
  - Accepts an optional JSON payload via --payload <json> or stdin ("-")
  - Prints JSON to stdout for the caller to parse
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from typing import Any, Dict, List, Optional


# ---------- Utility helpers ----------

def _read_payload(arg_value: str) -> Dict[str, Any]:
    """Read payload from a JSON string or stdin if '-' is passed."""
    if not arg_value:
        return {}
    if arg_value.strip() == "-":
        raw = sys.stdin.read()
    else:
        raw = arg_value
    if not raw.strip():
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        return {
            "__error__": f"Invalid JSON payload: {e}",
            "__raw__": raw,
        }


def _json_output(ok: bool, data: Any = None, error: Optional[str] = None) -> None:
    """Standard JSON output shape."""
    obj: Dict[str, Any] = {
        "ok": ok,
        "data": data,
    }
    if error is not None:
        obj["error"] = error
    json.dump(obj, sys.stdout, indent=2)
    sys.stdout.write("\n")
    sys.stdout.flush()


# ---------- Tool implementations ----------

def tool_find_gemini_cli(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Locate the Gemini CLI executable on this system.

    Strategy:
      - Use shutil.which on likely command names: ["gemini", "genai", "gcloud"]
      - Return:
          primary: best guess path or null
          candidates: list of {name, path}
          env_PATH: PATH used for search (for debugging)
    """
    candidate_names: List[str] = payload.get(
        "candidate_names",
        ["gemini", "genai", "gcloud"]
    )

    candidates: List[Dict[str, str]] = []
    for name in candidate_names:
        path = shutil.which(name)
        if path:
            candidates.append({"name": name, "path": path})

    primary_path: Optional[str] = candidates[0]["path"] if candidates else None

    return {
        "primary": primary_path,
        "candidates": candidates,
        "env_PATH": os.environ.get("PATH", ""),
        "note": (
            "primary is the first candidate found in PATH. "
            "If None, Gemini CLI is not currently discoverable."
        ),
    }


def tool_run_gemini_extensions(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    OPTIONAL helper: run a Gemini CLI 'extensions' subcommand.

    Payload fields (all optional):
      - exe: explicit path to Gemini CLI; if omitted, we auto-locate via tool_find_gemini_cli
      - subcommand: e.g. 'list' (default: 'list')
      - extra_args: list of extra CLI args, e.g. ["--help"]

    Example payload:
      { "subcommand": "list", "extra_args": ["--json"] }

    Returns:
      {
        "exe": "<path or null>",
        "command": ["gemini", "extensions", "list", ...],
        "returncode": <int or null>,
        "stdout": "<captured stdout>",
        "stderr": "<captured stderr>",
      }
    """
    exe: Optional[str] = payload.get("exe")
    subcommand: str = payload.get("subcommand", "list")
    extra_args: List[str] = payload.get("extra_args", [])

    if exe is None:
        # Reuse the locator
        info = tool_find_gemini_cli({})
        exe = info.get("primary")

        if exe is None:
            return {
                "exe": None,
                "command": None,
                "returncode": None,
                "stdout": "",
                "stderr": "Gemini CLI executable not found in PATH.",
            }

    cmd = [exe, "extensions", subcommand] + extra_args

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as e:
        return {
            "exe": exe,
            "command": cmd,
            "returncode": None,
            "stdout": "",
            "stderr": f"Failed to execute Gemini CLI: {e}",
        }

    return {
        "exe": exe,
        "command": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


# ---------- Tool router ----------

TOOL_REGISTRY = {
    "mcp.general_agent.find_gemini_cli": tool_find_gemini_cli,
    "mcp.general_agent.run_gemini_extensions": tool_run_gemini_extensions,
}


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="DOM/MCP tool wrapper for Gemini CLI-related operations."
    )
    parser.add_argument(
        "tool",
        help="Fully-qualified tool name (e.g. mcp.general_agent.find_gemini_cli)",
    )
    parser.add_argument(
        "--payload",
        default="{}",
        help='JSON payload string, or "-" to read JSON from stdin (default: "{}")', 
    )

    args = parser.parse_args(argv)

    payload = _read_payload(args.payload)

    if args.tool not in TOOL_REGISTRY:
        _json_output(
            False,
            data=None,
            error=f"Unknown tool: {args.tool}. Available: {list(TOOL_REGISTRY.keys())}",
        )
        return 1

    func = TOOL_REGISTRY[args.tool]

    try:
        result = func(payload)
        _json_output(True, data=result, error=None)
        return 0
    except Exception as e:
        _json_output(False, data=None, error=f"Exception in tool '{args.tool}': {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
