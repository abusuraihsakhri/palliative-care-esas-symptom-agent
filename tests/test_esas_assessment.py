"""Clinical item scoring regression tests independent of generic legacy engines."""
import pytest

from esas_palliative.assessment import SYMPTOMS, assess_scores


def test_all_zero_and_all_ten():
    assert assess_scores(dict.fromkeys(SYMPTOMS, 0))["total"] == 0
    result = assess_scores(dict.fromkeys(SYMPTOMS, 10))
    assert result["total"] == 90
    assert result["complete"] is True
    assert result["answered"] == 9


def test_missing_is_not_zero():
    result = assess_scores({"pain": 7})
    assert result["total"] is None
    assert result["scores"]["pain"] == 7
    assert result["scores"]["wellbeing"] is None
    assert result["answered"] == 1
    assert len(result["missing"]) == 8


def test_wellbeing_higher_means_worse():
    values = dict.fromkeys(SYMPTOMS, 0)
    values["wellbeing"] = 10
    assert assess_scores(values)["total"] == 10


@pytest.mark.parametrize("value", [-1, 11, 2.5, "4", True, float("nan"), float("inf")])
def test_invalid_rating(value):
    with pytest.raises(ValueError):
        assess_scores({"pain": value})


def test_unknown_key_and_wrong_payload():
    with pytest.raises(ValueError):
        assess_scores({"custom": 1})
    with pytest.raises(ValueError):
        assess_scores([])


def test_api_scores_when_api_dependencies_available():
    pytest.importorskip("fastapi")
    pytest.importorskip("httpx")
    from fastapi.testclient import TestClient
    from agents.api import app

    with TestClient(app) as client:
        complete = dict.fromkeys(SYMPTOMS, 0)
        response = client.post("/api/esas", json={"scores": complete})
        assert response.status_code == 200
        assert response.json()["total"] == 0
        invalid = client.post("/api/esas", json={"scores": {"pain": 11}})
        assert invalid.status_code == 422
        extra = client.post("/api/esas", json={"scores": {}, "other": "unexpected"})
        assert extra.status_code == 422
