"""FastAPI endpoints for legacy generic audits and ESAS-r symptom profiles."""
import os
from secrets import compare_digest
from typing import Dict, Optional

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, ConfigDict, StrictInt

from esas_palliative.assessment import assess_scores
from .base import AuditLogger
from .models import SystemTaskPayload
from .supervisor import SystemSupervisor

supervisor = SystemSupervisor(model_provider="mock")

app = FastAPI(
    title="Palliative Care ESAS Symptom Agent API",
    description="Legacy generic evaluation plus a separate descriptive ESAS-r rating endpoint.",
    version="3.0.1",
)


class ChatRequest(BaseModel):
    query: str


class ESASRequest(BaseModel):
    """No patient identifiers are accepted by this endpoint."""
    model_config = ConfigDict(extra="forbid")
    scores: Dict[str, Optional[StrictInt]]


@app.get("/health")
def health():
    return {"status": "HEALTHY", "service": "palliative-care-esas-symptom-agent", "version": "3.0.1"}


@app.get("/metrics")
def metrics():
    return {
        "dossiers_processed_total": len(supervisor.dossier_registry),
        "audit_blocks_total": len(AuditLogger.get_trail()),
        "format": "json",
    }


@app.post("/api/audit")
def api_audit(payload: SystemTaskPayload):
    """Compatibility endpoint; generic metrics, not an ESAS-r clinical assessment."""
    dossier = supervisor.process_task(payload)
    return dossier.to_dict()


@app.post("/api/esas")
def api_esas(req: ESASRequest):
    """Descriptive ESAS-r profile; incomplete profiles have a null total."""
    try:
        return assess_scores(req.scores)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/api/chat")
def api_chat(req: ChatRequest):
    try:
        return {"response": supervisor.query_supervisory_chat(req.query)}
    except Exception:
        raise HTTPException(status_code=400, detail="Unable to process supervisory query")


@app.get("/api/audit/logs")
def api_audit_logs(x_audit_token: Optional[str] = Header(default=None)):
    """Audit-log metadata is opt-in, not publicly exposed by default."""
    expected = os.getenv("ESAS_AUDIT_LOG_TOKEN")
    if not expected or not x_audit_token or not compare_digest(expected, x_audit_token):
        raise HTTPException(status_code=403, detail="Audit-log access is not authorized")
    return {"audit_trail": AuditLogger.get_trail(), "verified": AuditLogger.verify_integrity()}
