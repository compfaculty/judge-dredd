# Mathematics · research notebook v0.1

**Classification:** established mathematical tools mixed with unvalidated, proposed domain models. No court-ready numerical guilt or MSU inference exists.

## Variables and dimensions
- $\mathbf H$: harm vector (deaths: count; injuries: descriptors/durations; monetary loss: currency+date; deprivation: duration; rights claims: categorical). Do not add heterogeneous units without explicit assumptions.
- $S_\theta(x)$: context- and population-dependent latent severity (translation/location arbitrary; scale depends on choice model). NOT objective evil.
- $C_{a,e}$: role and culpability assessment (currently structured evidence, no validated scalar).
- $R(t,T)$: predictive future harm (not implemented, not estimable without validation).
- $U$: uncertainty distributions and missingness, not a universal confidence percentage.

## A. Bradley–Terry choice model (established method)
For cases $i,j$: $P(i\succ j)=\sigma(S_i-S_j)$ where $\sigma(z)=1/(1+e^{-z})$.
When the logistic scale is fixed, a one-unit *difference* changes choice odds by $e$. Use shared anchor cases for cross-population comparisons. Absolute origin is arbitrary. Tests: $P(i\succ i)=.5$ and $P(i\succ j)+P(j\succ i)=1$.

**MSU (provisional name):** unit difference in a fitted latent comparison model. No real-world calibration established. Never assert objective criminal severity from toy feature weights.

## B. Experimental feature map
$S_\theta(x)=\beta_0+\sum_k\beta_k\phi_k(x)+\sum_{k<l}\gamma_{kl}\phi_k(x)\phi_l(x)$.
Coefficients are unidentifiable without data, suitable comparisons, normalization and constraints. Fixed weights in `math_models.py` are only a synthetic demonstration.

## C. Bayesian evidence (established identity, unvalidated application)
$P(G\mid D)=P(D\mid G)P(G)/P(D)$.
Requires justified priors, likelihoods, and source-dependence modeling; cannot infer a guilt posterior from documents by assertion. Court's standard of proof is a legal rule, not a learned numeric threshold.

## D. Causal responsibility (research hypothesis)
A causal directed acyclic graph may include decisions, orders, effective control, knowledge, actions and consequences. Proposed $C_a=\sum_e q_\theta(e)\alpha_{a,e}$ is NOT a validated legal or moral formula. Multiple individuals can each be responsible for a single episode; never multiply victims.

## E. Dynamic analysis (not fitted)
$\frac{dH}{dt}=\lambda_H(t)$ for cumulative objectively defined harm, separately for dimensions. Observed historical estimates can decrease after evidence correction even when actual past harm does not.
$\frac{d\mathbf p}{dt}=\mathbf pQ(t)$ for a continuous-time Markov model, only if Markov assumption and transition rates are empirically defensible.
$R(t,T)=\int_t^{t+T}\sum_i p_i(\tau)h_i(\tau)d\tau$ is a prospective **hypothesis**, not a current risk score.
$\frac{dA}{dt}=\lambda_A-s-r$ remains dimensionally and normatively undefined: do NOT implement until the quantity and units are independently justified.

## F. Decision theory
$\arg\min_{a\in\mathcal A_{lawful}}\mathbb E[L(a,\omega)\mid D]$ is a conceptual research framework with rights/legality and required human review as hard constraints. Unknown costs and probability calibration preclude automated decisions.

## G. Descriptive moral evolution
$M_{descriptive}(x,c,t)$ depends on society, period, sampling, survey design and uncertainty. The normative core is reviewed by governed version changes, NOT auto-updated by polls. Time series/SDE models are proposals and need real evidence.

## H. Moral conflict and abstention
Multiple coherent normative models may disagree. Report ranking disagreement, uncertain evidence, legal conflicts and irreversibility separately. `HUMAN_REVIEW_REQUIRED` is a legitimate outcome, not a model failure.

## I. Verification boundaries
A correct formula may answer the wrong scientific question. Passing unit tests ≠ calibration; a judicial verdict is not known ground truth; agreement with one reviewer is not independent replication.
