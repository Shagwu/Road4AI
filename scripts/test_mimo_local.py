import json
import pathlib
import urllib.request

import yaml

PROJECT_FILE = pathlib.Path("project.yaml")


def load_project_config():
    with PROJECT_FILE.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_mimo_local(cfg):
    providers = cfg.get("providers", {})
    mimo = providers.get("mimo_local")
    if not mimo:
        raise SystemExit("mimo_local provider not found in project.yaml")
    return mimo["base_url"].rstrip("/"), mimo["model"]


def call_mimo_chat(base_url, model):
    url = f"{base_url}/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a concise assistant. Reply with exactly the user's requested text and nothing else."
            },
            {
                "role": "user",
                "content": "local MiMo is online"
            }
        ],
        "max_tokens": 32,
        "temperature": 0,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    cfg = load_project_config()
    base_url, model = get_mimo_local(cfg)
    print(f"Using mimo_local provider at {base_url}")
    print(f"Model: {model}")
    result = call_mimo_chat(base_url, model)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()