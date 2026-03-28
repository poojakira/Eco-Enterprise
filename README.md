# EcoTrack Enterprise — ESG Telemetry & Sustainability Ledger

**ESG telemetry nexus and cryptographic sustainability ledger — academic/personal project**

[![Industrial CI](https://github.com/poojakira/Eco-Enterprise/actions/workflows/ci.yml/badge.svg)](https://github.com/poojakira/Eco-Enterprise/actions)
[![Version: 8.5.0](https://img.shields.io/badge/version-8.5.0--STABLE-blue.svg)](./docs/RELEASES.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Coverage: 94%](https://img.shields.io/badge/coverage-94%25-brightgreen.svg)](https://github.com/poojakira/Eco-Enterprise)

**Async Ingestion** · **Merkle Ledger** · **Ensemble AI Forecasting** · **Anomaly Detection** · **Docker Deployment**

---

## 1. Overview

EcoTrack Enterprise is an ESG telemetry nexus and cryptographic sustainability ledger built as a hands-on learning project in async data pipelines, ML forecasting, cryptographic audit trails, and MLOps. It transforms fragmented carbon logs into an immutable, AI-optimized sustainability ledger.

### Key Features

- **Async Ingestion** — Producer-consumer pipeline; p99 latency 42 ms (baseline: 450 ms)
- **Merkle Ledger** — SHA-256 cryptographic audit trail; verifies 100,000+ records in <1s
- **Ensemble AI Forecasting** — Carbon footprint forecasting; MAE 4.2% (baseline: 14.2%)
- **Anomaly Detection** — 94.2% recall (baseline: 62%)
- **Multi-Environment Docker** — Dev / stage / prod profiles; 1-command `docker-compose up --build`

---

## 2. Architecture

The Nexus architecture uses a producer-consumer pattern and Merkle-tree anchoring for high-frequency telemetry (10^6 records/month).

> **[View Full System Diagram](docs/ARCHITECTURE.md)**

---

## 3. Benchmark Results

| Metric | Baseline (Sync/SQLite) | EcoTrack (Async/PG) | Improvement |
|---|---|---|---|
| **Ingestion Latency (p99)** | 450 ms | 42 ms | ~10.7x faster |
| **Verification Velocity** | 5.2s / 10k rows | 0.38s / 10k rows | ~13.6x faster |
| **Forecast Accuracy (MAE)** | 14.2% error | 4.2% error | ~70% improvement |
| **Anomaly Recall** | 62% | 94.2% | ~32.2% improvement |

> Note: Benchmarks measured in a local development environment. Results may vary in production.

---

## 4. Quick Start

```bash
git clone https://github.com/poojakira/Eco-Enterprise.git && cd Eco-Enterprise
export ENV=development
docker-compose up --build
```

| Service | URL |
|---|---|
| **API** (Swagger UI) | http://localhost:8000/docs |
| **Dashboard** | http://localhost:8501 |
| **Metrics** | http://localhost:8000/metrics |

---

## 5. API Endpoints

```bash
# Ingest Industrial Telemetry
curl -X POST "http://localhost:8000/api/v1/data/ingest" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '[{"sku_name": "Nexus-X", "carbon_footprint": 45.2, "region": "EU-West"}]'
```

---

## 6. Testing

```bash
pytest backend/tests/ -v --cov=backend
```

| Suite | Coverage |
|---|---|
| All tests | 94% coverage |

---

## 7. Documentation

| Domain | Specification |
|---|---|
| **Operations** | [CI/CD & GitHub Actions](.github/workflows/ci.yml) · [Observability](docs/OBSERVABILITY.md) |
| **Reliability** | [Failure-Mode Recovery](docs/FAILURE_MODES.md) · [Backup Strategy](docs/BACKUP_STRATEGY.md) |
| **Technical** | [Internals & Cryptography](docs/INTERNALS.md) · [ESG Dataset Schema](docs/DATASET.md) |
| **Strategy** | [Scalability](SCALING.md) · [User Personas & Workflows](docs/PERSONAS.md) |
| **Governance** | [Semantic Releases](docs/RELEASES.md) · [Security Specs](docs/SECURITY_SPECS.md) |
| **Experiments** | [Performance Analysis Notebook](notebooks/performance_analysis.ipynb) · [Full Metrics Report](docs/RESULTS.md) |

---

## 8. Team Contributions

> This is an academic/personal project built to learn async data pipelines, cryptographic audit systems, ML forecasting, and MLOps. Neither contributor has professional industry experience — all work was done as self-directed learning.

### Pooja Kiran

| # | What I Worked On | What I Built / Learned | Outcome |
|---|---|---|---|
| 1 | ESG Telemetry Ingestion Pipeline | Designed async producer-consumer ingestion architecture with PostgreSQL backend; learned async pipeline engineering | Ingestion latency p99: 42 ms (baseline: 450 ms) — 10.7x improvement |
| 2 | Cryptographic Merkle Ledger | Implemented SHA-256 Merkle-tree anchoring for carbon log verification; learned cryptographic audit trail design | Verification velocity: 0.38s / 10k rows (baseline: 5.2s) — 13.6x improvement |
| 3 | Ensemble AI Forecasting Engine | Built ensemble AI carbon footprint forecasting; integrated YAML Config Engine for multi-environment model selection | Forecast Accuracy (MAE): 4.2% error (baseline: 14.2%) — 70% improvement |
| 4 | Anomaly Detection System | Engineered anomaly detection pipeline with ensemble recall optimization | Anomaly Recall: 94.2% (baseline: 62%) — 32.2% improvement |
| 5 | Sustainability Recommendation Engine | Integrated Scope 3 hotspot identification and Action Center for sustainability recommendations | Recommendation engine fully integrated in Phase 12 |
| 6 | Dockerized Multi-Environment Deployment | Built Docker Compose infrastructure supporting dev, stage, and prod profiles | 3-environment Docker deployment; 1-command `docker-compose up --build` |
| 7 | Industrial Certification & Config Engine | Finalized YAML Config Engine, Production Checklist, and Scalability Strategy across Phase 12-16 | v8.5.0; 94% test coverage; 31 commits across 12+ development phases |
| 8 | Full Documentation Suite | Authored ARCHITECTURE.md, INTERNALS.md, OBSERVABILITY.md, FAILURE_MODES.md, BACKUP_STRATEGY.md, DATASET.md, PERSONAS.md, RELEASES.md, SECURITY_SPECS.md, USE_CASES.md, and RESULTS.md | 10+ formal specification documents |

### Rhutvik Pachghare

| # | What I Worked On | What I Built / Learned | Outcome |
|---|---|---|---|
| 1 | Pytest test suite | Wrote unit and integration tests across backend modules covering ingestion, verification, forecasting, and anomaly detection | 94% code coverage; all tests passing |
| 2 | Frontend dashboard | Built Streamlit dashboard (`frontend/`) showing real-time carbon telemetry, anomaly scores, and Merkle ledger entries | Dashboard accessible at localhost:8501 |
| 3 | CI/CD pipeline | Configured GitHub Actions workflow (`.github/workflows/ci.yml`) for lint, test, and Docker build on every push to main | CI pipeline runs automatically on each commit |
| 4 | Data scripts | Wrote data ingestion and ESG dataset preparation scripts in `scripts/` to load sample telemetry into PostgreSQL | Sample telemetry data loads successfully into the pipeline |
| 5 | CONTRIBUTING.md and CODE_OF_CONDUCT.md | Authored contributor documentation to standardize development workflow | Contributor guidelines documented for the project |

---

**Version**: 8.5.0 | **License**: MIT | **Coverage**: 94%
