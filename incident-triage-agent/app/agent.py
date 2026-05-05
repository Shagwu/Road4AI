# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import httpx
import google.auth
from typing import Optional, List, Dict, Any

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

try:
    _, project_id = google.auth.default()
except Exception:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "mock-project")

os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "True")

GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
MOCK_GITHUB = os.getenv("MOCK_GITHUB", "False").lower() == "true"

def _github_request(method: str, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
    if MOCK_GITHUB:
        if "search/code" in path:
            return {"items": [{"path": "src/controllers/user_controller.py", "repository": {"full_name": "google/adk"}}]}
        if "commits" in path:
            return [
                {"sha": "a1b2c3d4e5f6", "commit": {"message": "Add new auth validation logic", "author": {"name": "Alice"}}},
                {"sha": "e5f6g7h8i9j0", "commit": {"message": "Update dependency", "author": {"name": "Bob"}}}
            ]
        if "contents" in path:
            import base64
            return {"content": base64.b64encode(b"def user_handler():\n    return {'status': 'ok'}").decode('utf-8')}
        return {}

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "incident-triage-agent"
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    
    with httpx.Client(headers=headers, timeout=10.0) as client:
        response = client.request(method, f"{GITHUB_API_URL}/{path}", params=params)
        response.raise_for_status()
        return response.json()

def search_github_code(query: str) -> str:
    """Searches for code in GitHub repositories.
    
    Args:
        query: The search query (e.g., 'filename:app.py repo:owner/repo').
        
    Returns:
        A summary of search results.
    """
    try:
        results = _github_request("GET", "search/code", params={"q": query})
        items = results.get("items", [])
        if not items:
            return "No results found."
        summary = [f"Found {len(items)} files:"]
        for item in items[:5]:
            summary.append(f"- {item['path']} in {item['repository']['full_name']}")
        return "\n".join(summary)
    except Exception as e:
        return f"Error searching GitHub: {str(e)}"

def get_recent_commits(repo: str, path: Optional[str] = None) -> str:
    """Gets recent commits for a repository or a specific file.
    
    Args:
        repo: Repository in 'owner/repo' format.
        path: Optional file path to filter commits.
        
    Returns:
        A list of recent commit messages and authors.
    """
    try:
        path_query = f"/commits"
        params = {"per_page": 5}
        if path:
            params["path"] = path
        commits = _github_request("GET", f"repos/{repo}{path_query}", params=params)
        summary = [f"Recent commits for {repo}:"]
        for c in commits:
            msg = c['commit']['message'].split('\n')[0]
            summary.append(f"- {c['sha'][:7]}: {msg} by {c['commit']['author']['name']}")
        return "\n".join(summary)
    except Exception as e:
        return f"Error fetching commits: {str(e)}"

def read_github_file(repo: str, path: str) -> str:
    """Reads the content of a file from GitHub.
    
    Args:
        repo: Repository in 'owner/repo' format.
        path: Path to the file.
        
    Returns:
        The file content.
    """
    try:
        content = _github_request("GET", f"repos/{repo}/contents/{path}")
        import base64
        return base64.b64decode(content['content']).decode('utf-8')
    except Exception as e:
        return f"Error reading file: {str(e)}"

root_agent = Agent(
    name="incident_triage_agent",
    model=Gemini(
        model="gemini-flash-latest",
        temperature=0.0,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="""You are an expert Incident Triage Agent. Your goal is to help engineers diagnose and resolve production incidents.

When given an alert or incident description:
1. Summarize the likely cause by analyzing recent code changes (commits) in relevant areas of the codebase.
2. Use GitHub search to find relevant files, issues, or PRs.
3. Suggest diagnostic steps or potential fixes based on your analysis.
4. Be concise, technical, and prioritize safety. NEVER suggest destructive actions without a heavy warning.

If GITHUB_TOKEN is missing, inform the user that some features might be limited.
""",
    tools=[search_github_code, get_recent_commits, read_github_file],
)

app = App(
    root_agent=root_agent,
    name="app",
)
