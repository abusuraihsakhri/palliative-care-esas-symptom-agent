# Palliative Care ESAS Symptom Agent

A local-first symptom assessment interface based on the nine core domains of the **Edmonton Symptom Assessment System–revised (ESAS-r)**, with a Python scoring module and optional FastAPI endpoint.

The browser application is in [`web/`](web/). It works without Python, a backend, an account, or an internet connection once the static files have loaded. This project is an independent interface and is **not the official ESAS-r form or a validated clinical triage system**.

## ESAS-r assessment

- Rates **pain, tiredness, drowsiness, nausea, lack of appetite, shortness of breath, depression, anxiety, and wellbeing** on 0–10 integer scales.
- All scores are oriented in the same direction: **0 = none/best; 10 = worst possible**. A high *wellbeing* score therefore means **worse** wellbeing.
- Leaves unanswered items **missing**, not zero. A descriptive 0–90 total is shown **only with all nine ratings present**; individual scores remain visible.
- Supports an optional patient-defined symptom outside the nine-item total.
- Exports a local JSON or CSV report; optional printing. No automatic assessment history, server transmission, or database storage.
- Does **not** apply an unvalidated total-score severity cutoff, diagnose symptoms, or recommend medication or escalation.

A low total does not rule out a clinically important individual symptom. Use clinical judgment and the current ESAS-r administration guidance.

## Browser use

Serve the `web/` folder with any static web server (the app uses an ES module, so opening via `file://` may fail in browsers):

```bash
python -m http.server 8000 --directory web
```

Open `http://localhost:8000/`. Enter ratings, inspect the separate symptom values, and choose **Export JSON**, **Export CSV**, or **Print**. All nine core ratings must be present before the descriptive total is calculated; partial reports can still be exported with blanks.

The static app uses standard HTML, CSS, and native JavaScript modules. It requires no Pyodide, installation, external fonts, or remote service. Compatible with modern browsers supporting ES modules.

## Python scoring

Python 3.9+ is supported:

```bash
python -m pip install -e ".[api,test]"
python -m pytest -q
node --test web/esas-core.test.mjs  # optional; Node 22
```

```python
from esas_palliative.assessment import SYMPTOMS, assess_scores

values = dict.fromkeys(SYMPTOMS, 0)
values["pain"] = 7
profile = assess_scores(values)
assert profile["total"] == 7
```

Use the separately scoped REST endpoint for ESAS-r scores:

```bash
export AUDIT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
python cli.py serve --host 127.0.0.1 --port 8000

curl -s http://127.0.0.1:8000/api/esas \
  -H 'Content-Type: application/json' \
  -d '{"scores":{"pain":7,"tiredness":0,"drowsiness":0,"nausea":0,"lack_of_appetite":0,"shortness_of_breath":0,"depression":0,"anxiety":0,"wellbeing":0}}'
```

`POST /api/esas` requires a `scores` mapping. All values must be integers in 0–10 or `null`; absent items remain unassessed. Extra request fields or unexpected symptom names return HTTP 422. No identifying information is accepted by this endpoint.

### Compatibility interfaces

The repository also retains the earlier generic audit workflows: `python cli.py audit`, `python cli.py batch`, `python cli.py chat`, `python cli.py verify-audit`, and the installed `palliative-care-esas-symptom-agent` CLI (which uses `esas_palliative.cli`). The pre-existing `POST /api/audit` and `POST /api/chat` endpoints remain **generic metric evaluations, not implementations of the ESAS-r symptom scale**. Their arbitrary numeric thresholds and alerts must not be used for patient care.

The backend additionally exposes `GET /health`, `GET /metrics` (JSON counters), and `GET /api/audit/logs`. Audit-log retrieval is **disabled by default**; set `ESAS_AUDIT_LOG_TOKEN` on the API server and pass that value in the `X-Audit-Token` header to access it. HMAC signing of legacy audit records requires `AUDIT_SECRET_KEY` (an environment secret, never placed in browser code).

For containerized local runs, set `AUDIT_SECRET_KEY` in a private `.env` file and run `docker compose up --build`. The API is not intended to be exposed directly to the internet without access control, TLS, and a suitable institutional privacy/security review.

## Privacy and limitations

The browser application stores nothing persistently and makes no API calls. Data stays in the page until cleared or closed, except for report files users intentionally save or print. Avoid identifiers in the optional free-text symptom field if a report may be shared.

The optional Python server uses an in-memory registry for the generic legacy API and HMAC audit signatures. Its regex-based identifier checks are **not comprehensive de-identification**, nor a guarantee of HIPAA or other regulatory compliance. Do not input real patient-identifiable data into the generic endpoints without an institutional security assessment.

The app is a **symptom documentation aid**, not a medical device, emergency response system, clinical diagnostic service, or opioid dose converter. It does not replace professional assessment.

## References

- [Alberta Health Services — Symptom Assessment Tools (ESAS-r)](https://www.albertahealthservices.ca/info/page14546.aspx)
- [ESAS-r Administration Manual (Alberta Health Services)](https://www.albertahealthservices.ca/assets/info/peolc/if-peolc-ed-esasr-admin-manual.pdf)
- Watanabe SM et al. *J Pain Symptom Manage.* 2011;41(2):456–468. [DOI: 10.1016/j.jpainsymman.2010.04.020](https://doi.org/10.1016/j.jpainsymman.2010.04.020)

## License

[MIT](LICENSE).
