# Palliative Care ESAS Symptom Agent

> **Domain:** Clinical Decision Support & Biomedical Computing
> **Reference Standard:** Edmonton Symptympt Assessment System-revised (ESAS-r)

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

Palliative Care ESAS Symptom Agent is a clinical decision support system implementing the Edmonton Symptom Assessment System-revised (ESAS-r). It provides:

- **Symptom Score Evaluation**: Automated assessment of primary and secondary clinical metrics
- **Multi-Agent Consensus**: Three specialized workers evaluate payloads for QC invariants, safety boundaries, and protocol conformance
- **Risk Classification**: Multi-tier urgency classification (ROUTINE, ELEVATED, CRITICAL_STAT) with actionable recommendations
- **Tamper-Evident Audit Trail**: HMAC-SHA256 chained cryptographic audit logs for every evaluation
- **Zero-PHI Guard**: Active pattern detection blocking SSNs, MRNs, phone numbers, and patient identifiers from outbound data

---

## ⚙️ Architecture

```
agents/                      # Core multi-agent evaluation system
├── __init__.py              # Package init
├── api.py                   # FastAPI REST server
├── base.py                  # PHI Guard, HMAC-SHA256 Audit Trail
├── learning.py              # Bayesian calibration engine
├── llm_factory.py           # LLM provider abstraction
├── metrics.py               # Prometheus metrics exporter
├── models.py                # Pydantic data models with validation
├── streamer.py              # WebSocket telemetry broadcaster
├── supervisor.py            # Multi-agent orchestrator
└── workers.py               # Specialized evaluation workers

esas_palliative/             # ESAS-r domain-specific module
├── __init__.py
├── agents.py                # Domain-specific sub-agents
├── cli.py                   # CLI for ESAS module
├── engine.py                # Core domain evaluation logic
├── models.py                # Domain data models
└── server.py                # FastAPI server factory

cli.py                       # Main CLI entry point
enrichment.py                # Feature enrichment engines
simulator.py                 # High-throughput stress testing
web/index.html               # Operations console UI
```

---

## 💻 Installation

```bash
# Clone the repository
git clone https://github.com/abusuraihsakhri/palliative-care-esas-symptom-agent.git
cd palliative-care-esas-symptom-agent

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install fastapi uvicorn pydantic pytest

# Set required environment variable
export AUDIT_SECRET_KEY="your-secure-random-key-here"
```

---

## 🚀 Usage

### CLI Commands

```bash
# Run single task evaluation
python cli.py audit --task-id TASK-001 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT

# Interactive chat with supervisor
python cli.py chat "What is the system status?"

# Batch process CSV records
python cli.py batch -i sample.csv -o results.csv

# Verify audit trail integrity
python cli.py verify-audit

# Launch REST API server
python cli.py serve --host 127.0.0.1 --port 8000
```

### REST API

| Endpoint | Method | Description |
|:---------|:-------|:------------|
| `/health` | GET | Service health check |
| `/metrics` | GET | Operational metrics |
| `/api/audit` | POST | Submit task for evaluation |
| `/api/chat` | POST | Query supervisory chat |
| `/api/audit/logs` | GET | Retrieve audit trail |

### Example API Request

```bash
curl -X POST http://localhost:8000/api/audit \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "TASK-001",
    "target_identifier": "TARGET-01",
    "primary_metric": 28.4,
    "secondary_metric": 14.2,
    "is_critical_flag": true,
    "status_descriptor": "DISCORDANT"
  }'
```

---

## 🧪 Testing

```bash
# Set test environment variable
export AUDIT_SECRET_KEY="test-audit-key"

# Run full test suite
pytest -v

# Run with coverage
pytest -v --cov=agents --cov=esas_palliative

# Run stress simulation
python simulator.py 1000
```

---

## 🐳 Docker Deployment

```bash
# Create .env file
echo "AUDIT_SECRET_KEY=$(openssl rand -hex 32)" > .env

# Build and run
docker-compose up --build

# Or manual Docker
docker build -t palliative-care-esas-symptom-agent .
docker run -p 8000:8000 --env-file .env palliative-care-esas-symptom-agent
```

---

## 🛡️ Security Features

| Feature | Implementation |
|:--------|:---------------|
| **PHI Outbound Guard** | Regex patterns detect SSNs, MRNs, emails, phone numbers, DOBs, patient names |
| **Audit Trail** | HMAC-SHA256 chained blocks with tamper detection |
| **Input Validation** | Pydantic models with bounds checking and length limits |
| **Secret Management** | `AUDIT_SECRET_KEY` env var required; no hardcoded defaults |
| **Error Handling** | Graceful handling of file I/O errors, malformed CSV, invalid values |

---

## 📋 Environment Variables

| Variable | Required | Description |
|:---------|:---------|:------------|
| `AUDIT_SECRET_KEY` | Yes | Secret key for HMAC-SHA256 audit trail signing |
| `MODEL_PROVIDER` | No | LLM provider (mock, ollama, claude, openai). Default: mock |

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
