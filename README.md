# AgentForge

AgentForge is a Python-based multi-agent studio for generating software projects with specialized agent teams. It detects the requested stack, routes work to frontend, backend, database, test, documentation, DevOps, and security teams, then writes the generated output into the `output/` workspace.

## What it does

- Detects the target stack from the user prompt.
- Coordinates specialized agent teams for frontend, backend, database, tests, docs, DevOps, and security.
- Generates a runnable output workspace under `output/`.
- Supports lightweight and quality-oriented execution profiles.
- Uses environment-driven model routing for different agent roles.

## Project Layout

```text
project_agent.py        Main orchestration entrypoint
core/                   Shared config, model routing, skills, and tools
teams/                  Specialized agent teams by domain
skills/                 Reusable skill definitions for agents
.specify/               Spec-driven workflow assets and templates
specs/                  Feature specs and generated plan/task artifacts
output/                 Generated project output
```

## Requirements

- Python 3.11+ recommended
- Access to an OpenAI-compatible LLM endpoint or NVIDIA NIM
- Optional: Brave Search, GitHub token, database credentials, and other MCP-related environment variables

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and fill in the values you need.

## Configuration

The most common variables are:

- `NVIDIA_API_KEY` or `LLM_PROVIDER=ollama` with `OLLAMA_MODEL`
- `BRAVE_API_KEY`
- `GITHUB_PERSONAL_ACCESS_TOKEN`
- `DATABASE_URL`
- `MONGODB_URI`
- `REDIS_URL`
- `OUTPUT_DIR`
- `AGENTFORGE_PROFILE` with values `fast`, `quality`, or `full`

See [.env.example](.env.example) for the full list.

## Usage

Run the main orchestrator and describe what you want to build:

```bash
python project_agent.py
```

The app will:

1. Extract the likely stack from your request.
2. Build the necessary agent teams.
3. Generate the requested project output into `output/`.

For a simple frontend request, AgentForge can take a direct fast path. For broader requests, it coordinates multiple teams in parallel.

## Spec-Driven Workflow

This repository also includes Spec Kit workflow assets under `.specify/` and `.github/agents/`.

The lifecycle is:

1. `specify`
2. `plan`
3. `tasks`
4. `implement`

The implementation phase is intentionally locked to existing `plan.md` and `tasks.md` artifacts when they are present.

## Notes

- `output/` is used for generated artifacts.
- Local Python caches, virtual environments, and JavaScript dependencies are ignored through `.gitignore`.
- The repo is designed to be extended with additional specialized teams and skills.

