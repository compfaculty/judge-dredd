# Mathematical Auditor — Initial audit

| Construct | Formal correctness | Empirical validity | Implementation decision |
|---|---|---|---|
| Bayes identity | Established theorem | Priors/likelihoods unavailable | Documentation only |
| Bradley–Terry | Established probabilistic model | No fitted population/case data | Tested utility, label EXPERIMENTAL |
| Latent MSU | Coherent as difference scale, model-conditional | Uncalibrated; cross-cultural invariance unknown | No real-case score |
| Polynomial severity | Algebraically valid | Weights arbitrary, possible wrong ordering | Synthetic tests only |
| Causal-command coefficient | Unspecified mapping | No validated data | Graph design only |
| Historical harm ODE | Unit-consistent if hazard definition supplied | No fitted intensity | Research specification |
| Outstanding accountability ODE | Units and ontology unresolved | None | BLOCK implementation |
| Markov future risk | Established mathematical machinery | Markov assumptions/data missing | BLOCK production prediction |
| Moral SDE | Valid class of processes | No evidence of suitability | Research hypothesis |
| Normative core | Philosophy/governance, not theorem | No proof of universal ethical correctness | Versioned constraints |
| 0.00001% error target | Arithmetic: 1e-7 | No calibration evidence | Never claim achieved |

## Required model-card checklist

### Educational notebook, version 1.0

`notebooks/theory_and_math.ipynb` illustrates the existing Bradley–Terry utility,
synthetic polynomial feature map, and historical-harm equation. Its piecewise-constant
integration uses hours of lost service and days, with nonnegative rates in hours/day;
it introduces no new domain definition or fitted model. The notebook documents units,
identifiability, worked examples, baselines, failure modes, and executable property
checks. Inputs are synthetic; independent scientific review remains **pending**.
No accountability ODE, production risk prediction, or automated legal decision is added.

### Checklist

1. Identifier and version; established/adapted/hypothesis/validated.
2. Source references (DOI / stable URLs) or `NEW HYPOTHESIS`.
3. Mathematical definition, units and normalizations.
4. Assumptions, causal interpretation and identifiability.
5. Hand-worked example with expected numeric result.
6. Property tests, edge cases, numerical stability.
7. Data provenance, sampling, missingness and dataset shift.
8. Calibration, confidence / credibility intervals, sensitivity.
9. Negative controls, baseline comparison, independent review.
10. Failure modes, allowed uses and prohibited uses.

## Critical corrections from prior brainstorming
- Do not add latent severity scores over events unless scale has additive meaning with a meaningful baseline.
- Do not interpret logistic preference probability as probability that an allegation is true.
- Do not treat hypothetical expected-utility optimization as authorization of coercion.
- Do not infer a calibrated confidence estimate by formatting an LLM's judgment as a percentage.
- Do not encode ancient court judgments as objective moral ground truth.
- Human verdicts are feedback observations, not automatically correct labels.

## Reference starting points (check exact applicability)
- Bradley, R. A., Terry, M. E. (1952), *Rank Analysis of Incomplete Block Designs: I. The Method of Paired Comparisons*, Biometrika, DOI: 10.1093/biomet/39.3-4.324.
- Brier, G. W. (1950), *Verification of Forecasts Expressed in Terms of Probability*, Monthly Weather Review, DOI: 10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2.
- NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework

**Auditor must not self-certify:** a second implementation or qualified independent reviewer is required before claims of scientific validation.
