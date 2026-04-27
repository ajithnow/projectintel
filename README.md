<p align="center">
  <h1 align="center">🧠 Project Intelligence Engine</h1>
  <p align="center">
    Transform static project artifacts into an interactive AI‑powered reasoning engine.
    <br />
    <a href="#quick-start"><strong>Get Started »</strong></a>
    ·
    <a href="https://github.com/ajithnow/projectintel/issues">Report Bug</a>
    ·
    <a href="https://github.com/ajithnow/projectintel/issues">Request Feature</a>
  </p>
</p>

<p align="center">
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT" />
  </a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/python-3.13+-brightgreen.svg" alt="Python 3.13+" />
  </a>
  <a href="https://github.com/ajithnow/projectintel/blob/main/CONTRIBUTING.md">
    <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome" />
  </a>
</p>

---

## Overview

**Project Intelligence Engine** is a production‑grade, AI‑driven project management system that converts static artifacts — PRDs, architectural diagrams, call transcripts, and more — into an interactive reasoning engine using **Retrieval‑Augmented Generation (RAG)**.

It follows **hexagonal architecture**, **domain‑driven design**, and an **event‑driven asynchronous backbone** to ensure scalability, maintainability, and vendor independence.

## ✨ Key Features

| Feature | Description |
|---|---|
| **Provider‑agnostic LLM** | Swap model providers via a single config change (powered by LiteLLM). |
| **Async AI Pipelines** | Heavy AI work is decoupled from HTTP via Redis Streams + FastStream. |
| **Multi‑tenant Vector Store** | LanceDB with pre‑filtering ensures zero cross‑project data leakage. |
| **Multi‑Agent Orchestration** | LangGraph supervisor delegates to BA, PM, Developer, and Tester personas. |
| **Hallucination Firewall** | Pydantic AI enforces type‑safe, schema‑validated LLM outputs. |
| **Real‑time Updates** | WebSocket broadcasting pushes agent progress to the React Command Center. |
| **Empirical Estimation** | Reference Class Forecasting (RCF) grounds estimates in historical data. |

## 🏗️ Architecture

```
features/
├── auth/          # Authentication (routers, schemas, services)
├── core/          # Shared config, database engine, base schemas
└── users/         # User management (models, routers, schemas)
```

The codebase is organised by **feature modules**, each containing its own routers, schemas, models, and services. Shared infrastructure lives under `features/core/`.

## 🚀 Quick Start

### Prerequisites

| Tool | Version |
|---|---|
| Python | 3.13+ |
| PostgreSQL | 14+ |
| [uv](https://docs.astral.sh/uv/) | latest |

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/ajithnow/projectintel.git
cd projectintel

# 2. Create a virtual environment and install dependencies
uv sync

# 3. Copy the example env file and fill in your values
cp .env.example .env
```

### Environment Variables

| Variable | Description | Example |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+psycopg://user:pass@localhost:5432/projectintel` |
| `DEBUG` | Enable debug mode | `True` |

### Database Setup

```bash
# Run Alembic migrations
alembic upgrade head
```

### Run the Server

```bash
uvicorn main:app --reload
```

The API is now available at **http://localhost:8000**.

## 📖 API Documentation

| Interface | URL |
|---|---|
| Swagger UI | [/docs](http://localhost:8000/docs) |
| ReDoc | [/api-docs](http://localhost:8000/api-docs) |
| OpenAPI JSON | [/openapi.json](http://localhost:8000/openapi.json) |

## 🧪 Running Tests

```bash
# Run the full test suite
pytest

# With coverage
pytest --cov=features
```

## 🛠️ Tech Stack

| Concern | Technology |
|---|---|
| API Framework | FastAPI + Uvicorn (ASGI) |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Database | PostgreSQL (via psycopg) |
| Validation | Pydantic v2 |
| Config | pydantic‑settings |
| Package Manager | uv |

## 🗺️ Roadmap

See the [project plan](project.md) for the full implementation roadmap, including:

- [ ] Redis Streams + FastStream event backbone
- [ ] LanceDB vector store integration
- [ ] LangGraph multi‑agent orchestration
- [ ] Pydantic AI hallucination firewall
- [ ] React Command Center UI
- [ ] Reference Class Forecasting engine

## 🤝 Contributing

Contributions are what make the open source community amazing. Any contributions you make are **greatly appreciated**.

Please read our [Contributing Guide](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) before submitting a pull request.

## 📄 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.

## 🔒 Security

If you discover a security vulnerability, please follow our [Security Policy](SECURITY.md). **Do not open a public issue.**

## 📬 Contact

**Ajith** — [@ajithnow](https://github.com/ajithnow)

Project Link: [https://github.com/ajithnow/projectintel](https://github.com/ajithnow/projectintel)
