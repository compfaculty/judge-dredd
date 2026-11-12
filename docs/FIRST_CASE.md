# First real case: reproducible research workflow

## Source and scope

`us-eichman-1990` imports United States v. Eichman et al., No. 89-1433,
496 U.S. 310 (1990). The source is the [official Library of Congress PDF](https://tile.loc.gov/storage-services/service/ll/usrep/usrep496/usrep496310/usrep496310.pdf).
The opinion describes the charge at p. 312 § I, dismissal and direct appeal at
p. 313, the historical statute at p. 314, the constitutional dispute at p. 315,
the majority's reasoning at p. 318 and affirmance at p. 319.

Closed scope means the § 700 flag-burning charge in No. 89-1433. The
consolidated Haggerty proceeding, No. 89-1434, is excluded: p. 313 n. 1 explicitly
leaves a separate property charge pending. No later disposition of that charge
is asserted. No comprehensive subsequent docket or rehearing search was performed.
Affirmed dismissal is not a fact-trial acquittal or proof of innocence.

## Reproduce

```bash
pip install -e '.[dev]'
python -m judge_dredd.import_case
uvicorn judge_dredd.api:app --host 127.0.0.1
# http://127.0.0.1:8000/cases/us-eichman-1990/review
pytest -q
```

The bundled `src/judge_dredd/data/eichman/opinion.pdf` is the retained original.
`case.json` records URL, document identifier/version, retrieval time, SHA-256,
rights/retention notes, page anchors and editorial mappings. The statutory
reference is dated to the 1988 edition, Supplement I, as reproduced by the Court;
it is not a current-law lookup. The [GPO policy, Public Domain & Copyright Notice](https://www.govinfo.gov/about/policies)
explains the federal-government-work basis and the third-party-content caveat.
The retained material is an official federal judicial opinion; no blanket license
for unrelated collection content is inferred. No bulk scraping or private records.

Import performs no network requests. It checks file size/hash, page count,
nonempty page extraction and short location anchors before inserting records in
one transaction. It preserves 1-based PDF page numbers and printed reporter page
numbers (PDF page 1 = reporter 310). The report contains curated assertions,
evidence inventory, timeline, element coverage and limitations; these are not
produced by a trained legal model. The exact PDF is identity-checked, but a
verified source may still contain allegations. OCR/extraction anchors do not
verify the truth of a claim or replace independent legal review.

The initial `Assessment` stores model version, manifest hash and source metadata.
An `AuditEvent` stores its canonical JSON SHA-256. Reimport is idempotent and
rejects a changed manifest against an existing record; explicit revision tooling
is future work. Existing synthetic cases are preserved. The new SourceSnapshot
table is additive; no existing columns are altered. Database migrations remain
future work. Audit hashes detect changes when compared with a trusted copy;
ordinary database rows can be edited and do not form a tamper-proof ledger.

## Assessment and human form

The system's assessment is `ABSTAIN_ON_FACTUAL_GUILT`, always accompanied by
`HUMAN_REVIEW_REQUIRED`. Missing trial exhibits and independent factual inquiry
prevent a factual-guilt finding from this record. Probability, MSU and risk
remain `null`. No mathematics or moral-scale definitions were changed.
The element matrix separates statutory components, the disposal exception and
the constitutional barrier; its coverage labels are editorial interpretations,
not measurements of proof beyond reasonable doubt.

The official outcome is stored as `CourtJudgment` and exposed separately through
`/judgments`. This is **not blinded evaluation**: the curator had read the
outcome-bearing opinion, and extracted pages themselves reveal it. Hiding a UI
section does not remove that contamination. No accuracy/calibration claim follows.

The `/review` page displays sources and offers agree/disagree/need-more-evidence/
abstain with rationale. This is a review of the inventory, not a guilty/not-guilty
model verdict. POST `/reviews` requires the imported assessment's ID; missing,
unknown or other-case references are rejected. A HumanReview and AuditEvent are
saved together without changing the frozen report. GET `/reviews` retrieves
feedback. Reviewer names are self-declared; this is not authenticated independent
review. Candidate-model feedback has no ingestion path and is not stored as a
human review.

## Security and outstanding review

Use loopback locally. No authentication, reviewer-identity verification, CSRF
protection, concurrency-safe import retry or production access-control layer is
implemented. No arbitrary URL/file upload is exposed: only the fixed curated
package is imported. Browser rendering uses textContent for source and reviewer
content; it never renders source text as HTML. The original PDF remains untrusted
parser input, bounded and hash-checked; a hash is not proof of a harmless PDF.
Witness records, addresses and private exhibits were not added. Independent
legal review, source/extraction review and a truly blinded fact-rich case remain
open work. No model is scientifically validated by these tests.
