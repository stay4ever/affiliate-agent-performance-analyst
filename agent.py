#!/usr/bin/env python3
"""Affiliate Agent Performance Analyst — Nanoplasticity Agent"""

import os
import json
import requests

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None


def main():
    task = os.environ.get("TASK", "")
    run_id = os.environ.get("RUN_ID", "")
    callback_url = os.environ.get("CALLBACK_URL", "")
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")

    if not task:
        print("No TASK provided")
        return

    # ── Run your agent logic here ──────────────────────────
    result = run_agent(task, api_key)

    # ── Report results back to Nanoplasticity ─────────────
    if callback_url and run_id:
        requests.post(callback_url, json={
            "run_id": run_id,
            "status": "complete",
            "output": result
        }, timeout=30)

    print(json.dumps({"status": "complete", "output": result}, indent=2))


def run_agent(task: str, api_key: str) -> str:
    """
    Your agent logic goes here.

    This starter uses Claude to process the task.
    Replace or extend this with your own logic.
    """
    if not Anthropic or not api_key:
        return f"Echo: {task}"

    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{"role": "user", "content": task}]
    )
    return response.content[0].text


if __name__ == "__main__":
    main()
