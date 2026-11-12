# Human-in-the-loop protocol

Possible results: `ASSESSMENT_READY`, `INSUFFICIENT_EVIDENCE`, `MORAL_CONFLICT`, `HUMAN_REVIEW_REQUIRED`, `LEGAL_REVIEW_REQUIRED`.

- The researcher acts as a simulated jury/reviewer for experimentation, not as an actual jury or court.
- Maintain distinct artifacts: initial model prediction, human opinion, actual judgment, revision after appeal.
- Human verdict is observation, not unquestionable ground truth. Escalation does not transfer away responsibility for model errors.
- Serious criminal issues require qualified human/legal oversight; no model-enforced punishment or reprisal.
- Explain: which input triggered escalation, what is disputed, whether the issue is factual/legal/normative, and what further evidence matters.
- Preserve reviewer feedback in an audit event and never silently retrain from one individual's opinion.
- Protect privacy of victims and witnesses. Avoid personally identifying details unless needed and lawfully handled.
