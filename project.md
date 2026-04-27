# Project Intelligence Engine (v1.1)
## Actionable Technical Project Plan

> A production-grade, AI-driven project management system that leverages Retrieval-Augmented Generation (RAG) to convert static artifacts into an interactive reasoning engine.

---

## Overview

The Project Intelligence Engine (v1.1) represents a fundamental shift in how project management documentation is ingested, synthesized, and transformed into actionable operational intelligence. This plan details the architectural blueprint for converting static artifacts — ranging from PRDs and architectural diagrams to unstructured call transcripts — into an interactive reasoning engine.

The primary catalyst for the v1.1 revision is a strategic pivot toward a highly scalable cloud-based deployment methodology. Rather than relying on hardcoded model providers, the architecture implements a **provider-agnostic LLM adapter pattern** — allowing seamless request routing across any cloud model without rewriting business logic, preventing vendor lock-in, and enabling dynamic model selection based on cost or performance needs.

---

## 1. Foundational Architecture and Domain-Driven Design

The system strictly adheres to **Hexagonal Architecture** (Ports and Adapters) integrated within a **Domain-Driven Design (DDD)** methodology to insulate core business logic from third-party infrastructure volatility.

### Architectural Layers

| Layer | Responsibility |
|---|---|
| **Domain Layer** | Core entities (`Project`, `Task`, `Source`, `Persona`), domain events (`TranscriptIngested`, `EstimateRequested`), and all business rules. Zero external dependencies. |
| **Application Layer** | Orchestrates use cases (`GenerateProjectPlan`, `AnalyzeTechnicalRisk`). Interacts with the Domain Layer via abstract Ports. Unaware of storage or processing specifics. |
| **Infrastructure Layer** | Concrete Adapters fulfilling interface contracts — SQLAlchemy, LanceDB, Redis/FastStream, and LLM API clients. |

### Directory Matrix

| Directory Path | Responsibility |
|---|---|
| `src/domain/` | Pure Python entities, Value Objects, Domain Events. **No third-party imports.** |
| `src/application/` | Use case services and abstract Port definitions for repositories and AI services. |
| `src/infrastructure/` | Technology-specific implementations: `lancedb_repo.py`, `llm_api_adapter.py`, `redis_broker.py`. |
| `src/presentation/` | FastAPI routers, WebSocket managers, DI config, Pydantic HTTP schemas. |
| `src/main.py` | Composition Root — wires adapters to ports and initializes the FastAPI lifecycle. |

---

## 2. Event-Driven Asynchronous Backbone

AI integration introduces profound latency challenges. To resolve this, the engine **completely decouples heavy AI computations from the client-facing HTTP cycle** using an Event-Driven Architecture (EDA).

### Redis Streams and FastStream Integration

Redis Streams provide an **append-only, persistent event log** with consumer group support — solving the "fire-and-forget" limitation of traditional Pub/Sub.

**FastStream** abstracts raw message parsing using Pydantic for automatic serialization, deserialization, and validation of JSON event payloads — with auto-generated AsyncAPI documentation.

### Asynchronous Ingestion Pipeline

```
User Upload
    │
    ▼
FastAPI Endpoint ──► XADD to Redis Stream ──► HTTP 202 Accepted
                                │
                                ▼
                    FastStream Background Worker
                                │
                         ┌──────┴──────┐
                         │  Distiller  │
                         │  Pipeline   │
                         └──────┬──────┘
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                  ▼
        Parse Document    Extract Metadata    Chunk & Embed
              │                                    │
              └─────────────────┬──────────────────┘
                                ▼
                    Index into LanceDB Vector Store
                                │
                                ▼
                           XACK (Complete)
```

**Fault Tolerance:** Unacknowledged messages remain in pending state. A secondary worker reclaims them via `XAUTOCLAIM`, ensuring zero data loss.

### Real-Time WebSocket State Broadcasting

As the FastStream worker progresses through LangGraph nodes, it publishes state transition events. A dedicated WebSocket manager pushes granular progress payloads to the React "Command Center" UI — providing total visibility into the AI's reasoning phases.

---

## 3. Multimodal RAG and the LanceDB Lakehouse

### Why LanceDB

- Built natively in **Rust** using the Lance file format
- Lance format 2.2 introduces Blob V2 architecture, nested schema evolution, and advanced compression
- Up to **1,000× faster random access** vs. legacy formats like Parquet
- Exceptionally suited for enterprise RAG pipelines

### Multi-Project Isolation and Metadata Filtering

Every ingested chunk is tagged with an exhaustive metadata schema including a persistent `project_id`. The system enforces **Pre-Filtering** (`prefilter=True`) as the default:

```
WHERE project_id = 'P-104' AND source_type = 'ADR'
```

Pre-filtering restricts the ANN search space *before* vector similarity is calculated — preventing cross-project data leakage in multi-tenant deployments.

**Performance mandates:**
- Scalar indices on `project_id` and `document_category` for sub-50ms retrieval
- Multi-base path model for distributed S3 storage without metadata rewrites

### Retrieval Strategy

| Parameter | Configuration |
|---|---|
| **Distance Metric** | Dot product (fastest for normalized vectors) |
| **Chunk Size** | 1,024 tokens (empirically validated optimal balance) |
| **Top-K (Large Context)** | ~15,360 tokens of dense context for 100K+ token windows |

---

## 4. Multi-Agent Orchestration via LangGraph

The architecture replaces monolithic prompt engineering with a **Subagents (Centralized Orchestration)** pattern powered by LangGraph.

### Supervisor + Sub-Agent Architecture

```
Incoming Query
      │
      ▼
 ┌──────────┐
 │ Supervisor│ ◄── Decomposes query into discrete steps
 └─────┬────┘
       │
  ┌────┼────────────────────────────┐
  ▼    ▼          ▼                 ▼
 BA   PM       Developer         Tester
Persona Persona  Persona          Persona
```

### Sub-Agent Personas (Persona-Based Structured CoT)

**Business Analyst (BA)**
1. Isolate speakers, stakeholders, and themes from transcripts
2. Extract explicit business requirements and user constraints
3. Format into standardized Agile user stories

**Project Manager (PM)**
1. Extract status updates, blockers, and timelines
2. Identify cross-team dependencies and critical path vulnerabilities
3. Draft executive summaries and update the risk register

**Developer**
1. Retrieve and analyze ADRs and infrastructure diagrams
2. Enumerate technical constraints, payload schemas, and DB migrations
3. Generate granular, chronologically ordered technical task breakdowns

**Tester**
1. Analyze functional requirements from BA user stories
2. Define positive test paths and acceptance criteria
3. Engineer negative test paths, boundary conditions, and edge cases

Sub-agents are **completely stateless and isolated** — processing specialized prompts without interference from previous conversation turns.

---

## 5. The Hallucination Firewall via Pydantic AI

### Schema Enforcement

Pydantic AI defines rigid **data contracts** using `BaseModel` classes with deeply nested type hints. The `output_type` constraint mathematically forces the LLM to return data matching the defined schema — shifting from unstructured text generation to type-safe software engineering.

### Context-Driven Grounding Validation

Dynamic runtime contexts (retrieved document vectors, DB connections) are injected into the validation layer via `deps_type` and `ValidationInfo` objects.

**Example — Database Technology Validation:**
```
LLM suggests: "MongoDB"
Validator queries LanceDB ADRs → finds only "PostgreSQL" approved
@field_validator raises ValueError
```

### Autonomous Retry Loop

```
LLM Output ──► Pydantic Validator ──► PASS ──► Response
                       │
                      FAIL
                       │
              Re-prompt with error trace:
         "Validation Error: 'MongoDB' is not approved.
          Select from: [PostgreSQL]"
                       │
                       ▼
              LLM Self-Corrects ──► Re-validate
```

### Observability via Logfire

Span-based evaluation captures telemetry for every internal reasoning step, tool call, and retry loop — verifying the agent actually queried the vector database rather than relying on cached hallucinations.

---

## 6. Cloud Inference Strategy: Provider-Agnostic Adapter Pattern

The Infrastructure Layer uses a unified abstraction gateway (e.g., **LiteLLM**) as the concrete LLM Port implementation:

- Normalizes requests into a standard format across 100+ models
- Swap providers by changing a **single config variable** — zero domain code rewrites
- **Automatic fallback routing** on provider downtime or rate limiting
- **Cost-based routing** — cheaper models for summarization, frontier models for complex architectural reasoning

---

## 7. Empirical Estimation via Reference Class Forecasting

Traditional Agile estimation is plagued by **optimism bias**. The engine implements **Reference Class Forecasting (RCF)** — a statistical methodology endorsed by the American Planning Association.

### RCF Pipeline

```
EstimateRequested Event
          │
          ▼
  Convert task to vector
          │
          ▼
  Query LanceDB (completed_tasks only)
  Top-K = 3–5 most similar historical tasks
          │
          ▼
  Extract empirical metadata:
  - estimated_story_points
  - actual_time_to_completion
  - developer_seniority_level
  - documented delays / blockers
          │
          ▼
  Generate deterministic estimate:
  "Based on 4 similar DB migration tasks (avg 8 days actual vs
   4 days estimated), empirical estimate is calibrated to 8 days."
```

### Confidence Score

Derived from the **Dot product distance** of historical matches:
- High distance (novel task, weak precedents) → **Low confidence** → flags for manual review
- Low distance (strong historical match) → **High confidence**

---

## 8. Implementation Roadmap

### Phase 1: Core Infrastructure and EDA Initialization (Weeks 1–2)

- [ ] Establish Hexagonal folder matrix and FastAPI Composition Root
- [ ] Deploy Redis Streams and configure FastStream background workers
- [ ] Initialize LanceDB multi-base path architecture with scalar indexing on `project_id`
- [ ] Deploy unified LLM gateway adapter with fallback routes

### Phase 2: Agentic Orchestration and Firewall Deployment (Weeks 3–4)

- [ ] Implement LangGraph Supervisor architecture with stateless sub-agents (BA, PM, Developer, Tester)
- [ ] Construct Pydantic AI Hallucination Firewall with `ValidationInfo` validators
- [ ] Implement span-based evaluation via Logfire

### Phase 3: UI Integration and Cloud Optimization (Weeks 5–6)

- [ ] Develop React "Command Center" with real-time WebSocket integration
- [ ] Enable multimodal image pasting for vision-encoder ingestion
- [ ] Execute inference optimization pass — tune prompt lengths, chunk parameters, and Pydantic schemas for cost and latency

---

## Technology Stack Summary

| Concern | Technology |
|---|---|
| API Framework | FastAPI + Uvicorn (ASGI) |
| Message Broker | Redis Streams + FastStream |
| Vector Store | LanceDB (Lance format 2.2) |
| Agent Orchestration | LangGraph |
| Output Validation | Pydantic AI |
| Observability | Logfire (span-based) |
| LLM Gateway | LiteLLM (provider-agnostic) |
| Frontend | React ("Command Center") |
| Estimation Strategy | Reference Class Forecasting (RCF) |

---

*By adhering to this architectural specification, the organization will deploy a secure, hyper-performant, and factually grounded reasoning engine capable of fundamentally transforming the accuracy and efficiency of project management workflows.*
