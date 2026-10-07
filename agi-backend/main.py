"""Local Tech Unfiltered API and executive-suite health service."""

from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:latest")
HOST = os.getenv("AGI_HOST", "127.0.0.1")
PORT = int(os.getenv("AGI_PORT", "8787"))

AGENTS = {
    "georgeDubec": (
        "You are George Dubec, the ultimate networker for Tech Unfiltered. "
        "Connect people, ideas, and opportunities. Be warm, practical, concise, "
        "and focused on useful introductions and next steps."
    ),
    "joannCoffey": (
        "You are Joann Coffey, the builder of Tech Unfiltered and a systems creator. "
        "Turn ideas into clear, practical systems. Be direct, thoughtful, and focused "
        "on execution."
    ),
}

EXECUTIVE_SUITE = [
    {"id": "joannCoffey", "title": "Builder", "status": "local-ready"},
    {"id": "georgeDubec", "title": "Ultimate Networker", "status": "local-ready"},
]


def ollama_chat(agent: str, messages: list[dict[str, str]]) -> str:
    payload = json.dumps(
        {
            "model": OLLAMA_MODEL,
            "stream": False,
            "messages": [{"role": "system", "content": AGENTS[agent]}, *messages[-12:]],
        }
    ).encode()
    request = Request(
        f"{OLLAMA_BASE_URL}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=60) as response:
        result = json.load(response)
    content = result.get("message", {}).get("content", "").strip()
    if not content:
        raise RuntimeError("Ollama returned an empty response.")
    return content


def ollama_health() -> dict[str, Any]:
    try:
        with urlopen(f"{OLLAMA_BASE_URL}/api/tags", timeout=5) as response:
            models = json.load(response).get("models", [])
        names = [model.get("name") for model in models if model.get("name")]
        return {
            "status": "ready" if OLLAMA_MODEL in names else "model-missing",
            "model": OLLAMA_MODEL,
            "models": names,
        }
    except (HTTPError, URLError, TimeoutError, OSError) as error:
        return {"status": "unreachable", "model": OLLAMA_MODEL, "error": str(error)}


class ApiHandler(BaseHTTPRequestHandler):
    def _write_json(self, status: int, payload: dict[str, Any]) -> None:
        encoded = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if length > 1_000_000:
            raise ValueError("Request body is too large.")
        return json.loads(self.rfile.read(length))

    def do_GET(self) -> None:
        if self.path == "/health":
            health = ollama_health()
            self._write_json(
                200 if health["status"] == "ready" else 503,
                {
                    "service": "tech-unfiltered-agi",
                    "local": True,
                    "ollama": health,
                    "executiveSuite": EXECUTIVE_SUITE,
                },
            )
            return
        if self.path == "/api/executive/status":
            self._write_json(
                200,
                {
                    "local": True,
                    "builder": "Joann Coffey",
                    "networker": "George Dubec",
                    "agents": EXECUTIVE_SUITE,
                    "ollama": ollama_health(),
                },
            )
            return
        self._write_json(404, {"error": "Route not found."})

    def do_POST(self) -> None:
        if self.path not in {"/api/agent", "/api/executive/chat"}:
            self._write_json(404, {"error": "Route not found."})
            return
        try:
            body = self._read_json()
            agent = body.get("agent", "georgeDubec")
            messages = body.get("messages", [])
            if agent not in AGENTS or not isinstance(messages, list) or not messages:
                raise ValueError("A valid agent and at least one message are required.")
            clean_messages = [
                item
                for item in messages
                if isinstance(item, dict)
                and item.get("role") in {"user", "assistant"}
                and isinstance(item.get("content"), str)
                and item["content"].strip()
            ]
            if not clean_messages:
                raise ValueError("At least one valid message is required.")
            content = ollama_chat(agent, clean_messages)
            self._write_json(
                200,
                {"content": content, "model": OLLAMA_MODEL, "local": True, "agent": agent},
            )
        except ValueError as error:
            self._write_json(400, {"error": str(error)})
        except (HTTPError, URLError, TimeoutError, OSError, RuntimeError) as error:
            self._write_json(503, {"error": f"Local Ollama request failed: {error}"})

    def log_message(self, format: str, *args: object) -> None:
        print(f"[agi-api] {format % args}")


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), ApiHandler)
    print(f"Tech Unfiltered local API listening on http://{HOST}:{PORT}")
    print(f"Using Ollama model: {OLLAMA_MODEL}")
    server.serve_forever()


if __name__ == "__main__":
    main()
