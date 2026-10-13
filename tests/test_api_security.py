"""Audit-log access must be explicitly enabled; defaults must not leak logs."""
import pytest


def test_audit_logs_not_public(monkeypatch):
    pytest.importorskip("httpx")
    from fastapi.testclient import TestClient
    from agents.api import app

    monkeypatch.delenv("ESAS_AUDIT_LOG_TOKEN", raising=False)
    with TestClient(app) as client:
        assert client.get("/api/audit/logs").status_code == 403
        monkeypatch.setenv("ESAS_AUDIT_LOG_TOKEN", "private-test-token")
        assert client.get("/api/audit/logs").status_code == 403
        assert client.get("/api/audit/logs", headers={"X-Audit-Token": "wrong"}).status_code == 403
        response = client.get("/api/audit/logs", headers={"X-Audit-Token": "private-test-token"})
        assert response.status_code == 200
        assert response.json()["verified"] is True
