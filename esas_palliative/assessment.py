"""Deterministic ESAS-r symptom profile; no diagnosis, triage, or treatment advice.

The nine core Edmonton Symptom Assessment System–revised (ESAS-r) items
are scored from 0 (none/best) to 10 (worst). In particular, a higher
wellbeing value denotes *worse* wellbeing. Unanswered items remain missing;
a nine-item total is calculated only when all nine have been recorded.
"""
from typing import Any, Dict, Mapping

SYMPTOMS = (
    "pain",
    "tiredness",
    "drowsiness",
    "nausea",
    "lack_of_appetite",
    "shortness_of_breath",
    "depression",
    "anxiety",
    "wellbeing",
)


def assess_scores(values: Mapping[str, Any]) -> Dict[str, Any]:
    """Validate an ESAS-r profile and return its descriptive (not triage) summary.

    A missing or null rating is unassessed, never implicitly zero.
    Raises ValueError for unknown items and invalid scores; booleans, floats,
    numeric strings, and out-of-range values are rejected.
    """
    if not isinstance(values, Mapping):
        raise ValueError("scores must be an object mapping symptom names to ratings")

    unknown = set(values) - set(SYMPTOMS)
    if unknown:
        raise ValueError("Unknown symptom(s): " + ", ".join(sorted(map(str, unknown))))

    scores: Dict[str, Any] = {}
    for symptom in SYMPTOMS:
        value = values.get(symptom)
        if value is not None and (type(value) is not int or not 0 <= value <= 10):
            raise ValueError(f"{symptom} must be an integer from 0 to 10 or null")
        scores[symptom] = value

    missing = [symptom for symptom in SYMPTOMS if scores[symptom] is None]
    total = sum(scores.values()) if not missing else None
    return {
        "instrument": "ESAS-r",
        "scores": scores,
        "answered": 9 - len(missing),
        "complete": not missing,
        "missing": missing,
        "total": total,
        "maximum_total": 90,
        "interpretation": "Descriptive symptom profile only; no validated total-score triage cutoff is applied.",
    }
