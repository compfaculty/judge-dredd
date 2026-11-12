# Case ontology and schema

## Implemented tables
`Subject`, `Case`, `Event`, `Charge`, `Evidence`, `Assertion`, `CourtJudgment`, `Assessment`, `HumanReview`, `ModelVersion`, `AuditEvent`, `SourceSnapshot` (metadata and extracted pages).

## Planned additions
`Victim` (privacy-controlled, pseudonymous), `Harm` (separate measured units and distributions), `ResponsibilityEdge` (actor→order→action→harm), `LegalRuleVersion`, `EvidenceDependency`, `ModelCard`, `FeedbackCandidate`, `Appeal`, `NormativeReview`.

## Evidence statuses
- `alleged`: allegation, not finding
- `disputed`: contested factual claim
- `court_established`: supported by referenced judicial finding, with court/date/status
- `researcher_claim`: researcher interpretation, not adjudicated

Evidence source status is different: `unverified`, `verified`, `synthetic`, etc. A verified source can still contain an allegation.

## Real-case workflow (first record: `us-eichman-1990`)
1. Record case ID, court and legal jurisdiction.
2. Collect judicial document with official URL and page/paragraph.
3. Extract factual assertions individually; link each to source.
4. Record criminal charges and statutory elements.
5. Record disposition and appeal status, separately from pre-verdict analysis.
6. Freeze assessment/model version and human-review response.

## No group liability
Citizenship and involuntary tax payments are not individual war-crime evidence. Track state reparations and individual responsibility as separate entities. Political opinion by itself is not a harm measurement.
