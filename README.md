# JUDGE DREDD — Evidence-Based Justice Research Engine

**Status:** early research prototype / scaffold, not a court or autonomous sentencing tool.

This repository starts a reproducible system for analyzing **documented criminal cases** with evidence provenance, separation of allegations from court-established facts, explicit uncertainty, human review, and careful mathematical auditing.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
python -m judge_dredd.seed_demo
python -m judge_dredd.import_case
uvicorn judge_dredd.api:app --reload
# Open http://127.0.0.1:8000/docs
pytest -q
```

The optional `demo-001` remains **synthetic**. `import_case` loads the bundled official PDF and curated record for **United States v. Eichman**, No. 89-1433 (1990), without network access. Open http://127.0.0.1:8000/cases/us-eichman-1990/review for the evidence inventory, element matrix, source pages, timeline, limitations and human assessment form. See [first-case provenance and scope](docs/FIRST_CASE.md).

SQLite works out of the box. Set `DREDD_DATABASE_URL=postgresql+psycopg://...` for PostgreSQL (see `compose.yaml`).

## Current implemented functionality

- Structured database models: subjects, cases, events, allegations/charges, evidence, assertions with provenance/status, court judgments, assessments, human reviews, model versions and audit events.
- `GET /health`, `GET /cases`, `GET /cases/{case_id}`, `GET /cases/{case_id}/assessment`, `POST /cases/{case_id}/reviews`.
- No inferred guilty verdict, sentencing recommendation or fabricated posterior probability. Assessment endpoint creates a **source-backed inventory with review required**.
- A separate **experimental** Bradley–Terry probability function and configurable toy severity score, explicitly NOT calibrated moral units.
- Math tests (normalization, antisymmetry, monotonicity), evidence status checks and API integration tests.
- Atomic, idempotent real-case import; PDF SHA-256 validation, page extraction, frozen versioned report and audit hash. Human reviews must reference the same case's saved assessment.
- `GET /cases/{case_id}/review`, `/sources/{page_number}`, `/judgments`, `/reviews` keep extracted pages, official outcome and researcher feedback accessible separately.

## Development workflow

### Interactive theory notebook

Open [Theory and Mathematics Laboratory](notebooks/theory_and_math.ipynb) for a guided
presentation with sliders, sensitivity plots, and a read-only source explorer.
All numerical examples are explicitly synthetic; no real-case scoring is performed.

```bash
source .venv/bin/activate
pip install -e '.[dev,notebook]'
jupyter lab notebooks/theory_and_math.ipynb
```

Select the kernel from this virtual environment, then run all cells. Controls require
a running kernel; default plots remain visible in the executed notebook. The notebook
does not modify the database or fetch sources. See [notebooks/README.md](notebooks/README.md)
for reproducibility checks and HTML export.

### Case research workflow

1. Read `AGENTS.md` and `docs/ROADMAP.md`.
2. Read `docs/ORIGINAL_GLOBAL_MORAL_ATLAS_NOTES.md` for archived discussions, and `docs/MATH_AUDIT.md` before adding any formula.
3. Import one **real, closed, published** case with primary source URLs + pinpoint references.
4. Capture model assessment *before* revealing the court's disposition to evaluation (when feasible).
5. Record researcher feedback separately from actual judgment; never treat agreement as independent validation.

## Scope and boundaries

- No autonomous verdict, imprisonment, force or enforcement; no legal advice claims.
- No guilt based solely on nationality, taxes, ethnicity, political affiliation or group membership.
- Serious/criminal decisions are always routed for human/legal review.
- Separate descriptive moral change, normative constraints, legal rules, evidence and empirical forecasts.
- No claim of individual 99.99999% certainty or valid MSU calibration without real experimental evidence.

See `docs/ARCHITECTURE.md`, `docs/CASE_SCHEMA.md`, `docs/EXPERIMENTS.md` and `docs/SOURCES.md`.

Run locally on loopback only. Authentication, authorization of reviewer identity and CSRF protection are not implemented; this prototype is not ready for shared or public deployment. Audit records are ordinary database rows, not a tamper-proof ledger.
