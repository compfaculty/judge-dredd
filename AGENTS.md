# Codex / coding-agent instructions

## Project language
All project files must be written in English, including documentation, comments, UI text, examples, and tests.

## Objective
Build an evidence-grounded **research** engine from real, publicly documented cases. Prioritize a complete, reproducible case workflow over complex theoretical modeling.

## Non-negotiable requirements
1. **Source every factual assertion.** Store citation URL/document ID, specific page/paragraph and evidence status. Never relabel an allegation as court-established without an identifiable judicial finding.
2. **No autonomous criminal verdicts, sentencing or punitive actions.** AI outputs are non-binding assessments with `HUMAN_REVIEW_REQUIRED` in serious matters.
3. **No fabricated probabilities or scores.** If no calibrated model exists, return `null` with clear explanation. Experimental toy scales must be prominently marked as such.
4. **Distinguish** (a) ground truth unavailable, (b) criminal-law standards, (c) normative judgments, (d) predictive estimates, (e) uncertainty.
5. **No group guilt.** Mandatory taxation or nationality alone does not establish a person's criminal liability.
6. Store independent human review, official judgments, and candidate-model feedback as different entities.
7. Historical law must be versioned and dated; changing descriptive attitudes does not update legal rules automatically.
8. Review any new mathematics against `docs/MATH_AUDIT.md`; demonstrate units, assumptions, identifiability, property tests, baselines and independent review status.
9. Prefer Python 3.12+, FastAPI, SQLAlchemy, Pydantic, PostgreSQL; SQLite fallback, pytest. Modular monolith, HTMX UI when ready.
10. Keep changes small, add regression tests and update docs. Never silently rewrite mathematical definitions; record revisions.

## First deliverable
Import one published *closed* criminal case using court documents. Generate an evidence inventory, charge-element coverage table, timeline, uncertainty/limitations and human-review form. Compare with official verdict only after initial assessment is frozen where feasible.

## Definition of done for a case
- Primary source document and pinpoint references
- Explicit procedural status and appeal history
- Distinct alleged vs established vs disputed facts
- No invisible leaps from evidence to guilt
- Reproducible assessment snapshot with model version
- Human-review recording and audit trail
- Tests for extraction and report consistency
