# Architecture · v0.1

## Pipeline

Case intake → primary-source evidence store → atomic assertions with legal/evidentiary status → timeline / causal graph → charge-element reasoning → uncertainty / model-card checks → explanation → human review → frozen comparison with actual court outcome → controlled feedback.

## Modules

- **Data ingestion:** PDFs, published judgments, source metadata, licensing, provenance. Future implementation, no PDF parser yet.
- **Ontology:** Person/organization, case, event, charge, evidence, assertion, victim/harm, responsibility edges, legal context.
- **Inference:** Never conflate objective harm, inferred causal contribution, legal elements, normative severity, risk.
- **Mathematical Auditor:** Dimensions, assumptions, test cases, sensitivity, empirical calibration, peer review.
- **Moral Invariant Core:** Versioned normative constraints; never silently drift with poll results.
- **Descriptive Moral Atlas:** Time-, society- and sampling-specific distribution of preferences.
- **Moral Conflict Detector:** Contrast normalized outputs; use human referral and explain what conflicts.
- **Human Review Gateway:** Record opinion separately from judicial decision; no automated binding outcomes.
- **Decision Provenance Ledger:** Tamper-evident design planned; current audit table is append-only by convention, NOT tamper-proof.

## Do not confuse
- Legal evidence standard ≠ model's posterior probability.
- Historical judgment ≠ known ground truth.
- Trial verdict ≠ representative moral preference.
- Severity score ≠ sentence length.
- Personal causal contribution ≠ guilt by job title.
- Observed societal preferences ≠ normative legitimacy.

## API implemented
- `GET /health`
- `GET /cases`
- `GET /cases/{case_id}`
- `GET /cases/{case_id}/assessment` (inventory, not adjudication)
- `POST /cases/{case_id}/reviews` (opinions: agree/disagree/need_more_evidence/abstain)

## Next milestones
Add Alembic migrations, file hash verification, source/pinpoint validation, structured proof-of-elements, frozen model snapshots, role-based access, privacy redaction, comparison UI and reproducible ingestion pipelines.
