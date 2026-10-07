# Tech Unfiltered AGI 🚀

> An open-source, zero-trust autonomous media network built on Next.js, LiteRT, and local LLMs.

![Tech Unfiltered](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-blue)
![Framework](https://img.shields.io/badge/Framework-Next.js-black)
![AI](https://img.shields.io/badge/AI-Ollama%20%7C%20CrewAI-orange)

Welcome to the **Tech Unfiltered AGI** repository. This project powers a completely autonomous tech media empire. It is designed to autonomously scrape tech news, evaluate hype versus reality, and generate high-quality podcast scripts and media—all wrapped in a highly-polished, cinematic web experience.

## Builder

**Joann Coffey is the builder of Tech Unfiltered.** George Dubec and Joann Coffey
remain separate agent choices in the public experience: Joann represents the
build-and-systems perspective, while George Dubec is the ultimate networker who
connects people, ideas, and opportunities.

## 🏗️ Architecture

This is a massive monolithic repository containing both the frontend and the highly secure backend mesh network.

1. **/tech-unfiltered**
   - The beautiful, cinematic **Next.js** frontend. Features glassmorphism, fluid animations (Framer Motion), and live telemetry dashboards.
   - The agent chat calls the same-origin `/api/agent` route, which securely bridges requests to local Ollama without exposing a cloud API key in the browser.
2. **/agi-backend**
   - The AI brain of the operation. It includes a small Python standard-library API
     for local chat and executive-suite health, plus the optional Docker Compose
     services that orchestrate:
     - **Ollama**: Local, private LLM execution.
     - **ChromaDB**: Long-term memory vector database.
     - **CrewAI & Crawlee**: Autonomous agents that scrape and write scripts (Python 3.11).
     - **Prometheus & Grafana**: Telemetry and metrics monitoring.
3. **/agi-backend/headscale**
   - A zero-trust **Headscale/Tailscale** mesh network that perfectly encrypts and isolates all internal database traffic.

## 🚀 Quickstart

We've containerized the entire backend infrastructure so you can launch it with a single command.

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/tech-unfiltered-agi.git
cd tech-unfiltered-agi

# 2. Launch the AI Backend (Docker required)
cd agi-backend
docker compose up -d --build

# The local executive API is available at http://127.0.0.1:8787
# Check it with:
curl http://127.0.0.1:8787/health

# 3. Launch the Frontend
cd ../tech-unfiltered
npm install
npm run dev
```

By default, the chat bridge uses Ollama at `http://127.0.0.1:11434` with
`llama3.2:latest`. To use another local Ollama endpoint or model, set
`OLLAMA_BASE_URL` and/or `OLLAMA_MODEL` in `tech-unfiltered/.env.local`.

### Local executive API

The frontend can call the Python API instead of connecting to Ollama directly.
This keeps the browser-to-model path on the local machine and exposes no API key:

```bash
cd agi-backend
python3 main.py
```

The API listens on `http://127.0.0.1:8787` and provides:

| Endpoint | Purpose |
| --- | --- |
| `GET /health` | Ollama and executive-suite health |
| `GET /api/executive/status` | Builder/networker identities and model status |
| `POST /api/agent` | Local George or Joann chat |
| `POST /api/executive/chat` | Alias for executive chat |

Set `AGI_BACKEND_URL=http://127.0.0.1:8787` in
`tech-unfiltered/.env.local` when the frontend should route through this API.
If it is unset, the Next.js route calls local Ollama directly.

When started with Docker Compose, the Python API starts automatically as the
`agi-workers` service. Its host port is bound to `127.0.0.1` only.

The model `glm-5.2:cloud` is intentionally not used by the default configuration:
it is a remote model and is not part of the free/local-only workflow.

## 🧰 VS Code setup

Open the repository root in VS Code, not only the frontend folder:

```bash
code .
```

VS Code will offer the recommended extensions listed in `.vscode/extensions.json`.
The workspace is configured for an open-source-friendly workflow:

- **Continue** can connect to a local Ollama model instead of a hosted coding assistant.
- **ESLint** and the TypeScript language service support the Next.js frontend.
- **Python** and **Pylance** support the backend.
- **Docker** manages the local AI services.

Use the Command Palette (`Cmd+Shift+P`) and choose **Tasks: Run Task**:

| Task | Purpose |
| --- | --- |
| `Frontend: dev server` | Start the Next.js app |
| `Frontend: lint` | Check frontend code |
| `Frontend: build` | Create a production build |
| `Backend: start local stack` | Start Ollama, ChromaDB, workers, and monitoring |
| `Backend: stop local stack` | Stop the Docker stack |

The paid video platform is separate from this open-source development stack. The
website and agent orchestration can be owned here while specialized video
generation remains an optional production service.

## 🤝 Contributing

We welcome pull requests, bug reports, and new agent ideas! Check out [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to get started.

## 📜 License

This project is licensed under the [MIT License](LICENSE).
