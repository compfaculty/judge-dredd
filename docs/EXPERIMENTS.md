# Experimental plan

## JD-001 — Single real closed case
Collect primary court judgment and evidence references. Blind initial assessment to final verdict when feasible; then compare factual extraction, charge-element mapping, missing evidence and human opinion. **No scoring of uncalibrated guilt.**

## JD-002 — Three-case benchmark
1. Direct perpetrator of intentional killing.
2. Commander / organizer adjudicated for subordinate crimes.
3. Mitigating-circumstances or contested-role case.

Verify publication, final status, stable primary sources and legal elements. Avoid leakage between training and evaluation. Record appeal history. Use court findings as procedural comparison, not metaphysical ground truth.

## JD-003 — Pairwise morality experiment
Synthetic cases with controlled features; 1,000 virtual raters and held-out preference pairs. Compare BT, hierarchical, and multidimensional / partial-order models; verify parameter recovery and calibrated predictive probabilities. Real human survey later, with ethics/privacy review.

## JD-004 — Error simulation
Synthetic truth, correlated evidence, different prevalence and reliability; evaluate false positives, false negatives, calibration, abstention, and cost-sensitive decisions. A 1e-7 error target cannot be asserted without large *independent representative* validation and systematic-risk analysis.

## JD-005 — Moral drift
Synthetic slow and abrupt change, polarized subpopulations, noisy verdict feedback and adversarial manipulation; detect descriptive drift without altering normative constraints. Measure rollback efficacy and catastrophic forgetting.

## Evaluation metrics
- Citation precision and unsupported-claim rate.
- Extraction recall vs adjudicated source text.
- Calibration curves, Brier score, uncertainty coverage (only with genuine probabilistic labels).
- Fairness/counterfactual identity tests (preserve legally relevant context).
- Escalation false-negative rate; reviewer disagreement and audit completeness.
- Blind comparison, dataset provenance, data leakage checks.

## Research guardrails
Human review for serious cases; model improvements can be proposed automatically but cannot be deployed based on one review. Do not confuse group-level outcomes with individual culpability.
