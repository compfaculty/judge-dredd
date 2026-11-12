# Global Moral Atlas — A Dynamic Mathematical Model of Crime, Responsibility, and Punishment

## 1. Project objective

Develop a mathematical and computational model capable of quantitatively assessing:

- The severity of a crime and the harm caused.
- The personal responsibility of the offender.
- Intent, motives, circumstances, and role in the crime.
- The accumulation of responsibility over time.
- The probability of reoffending and future danger to society.
- Remorse, cooperation with investigators, compensation, and behavioral reform.
- Historical and contemporary punishment practices in different countries.
- Different societies' moral views on justice and proportionality of punishment.

**Central idea:** assessment should be dynamic, mathematically grounded, empirically calibrated, and able to change as new evidence arrives.

The model must not confuse descriptions of public attitudes with legal authorization for violence. Its practical outputs are assessments of responsibility, risk, and proportionate legal measures.

## 2. Philosophical foundations

### 2.1. Morality can be formalized

The objective is to make moral parameters explicit, comparable, and suitable for analysis rather than exclude morality from calculations.

Moral judgments can be studied statistically, although numbers alone do not establish their objective correctness.

### 2.2. Retribution and prevention coexist

Punishment can serve several functions simultaneously:

- Accountability for past actions (*retribution*).
- Preventing future harm (*prevention*).
- Protecting society (*incapacitation*).
- Rehabilitation (*rehabilitation*).
- Restoring justice (*restorative justice*).

These functions are not mutually exclusive.

### 2.3. Responsibility for the past and future danger are distinct quantities

A person may remain responsible for serious crimes while no longer posing a danger.

Conversely, a person with little established culpability may require lawful preventive measures because of a specific current threat.

Past harm does not disappear through remorse.

### 2.4. Good deeds do not necessarily offset crimes

Two approaches need to be formally compared:

- **Utilitarianism:** aggregating positive and negative consequences.
- **Deontology:** certain violations cannot be canceled out by subsequent good deeds.

The model should support both normative approaches for comparative analysis rather than conceal the choice of one of them.

## 3. Crime feature matrix

Each case is described by a structured feature vector.

| Category | Parameters |
|---|---|
| Harm | Deaths, injuries, property damage, psychological consequences |
| Intent | Negligence, conscious risk-taking, direct intent |
| Motive | Revenge, personal gain, coercion, ideology, sadism |
| Role | Perpetrator, organizer, instigator, accomplice |
| Victims | Number, vulnerability, civilian status |
| Circumstances | Planning, repeated offenses, abuse of power |
| Criminal capacity | Legally established effect of mental condition |
| After the crime | Remorse, cooperation, compensation, repeated violations |
| Evidence | Reliability, independence, contradictions, procedural status |
| Judicial outcome | Legal classification, verdict, sentence length, appeal |

Facts, assumptions, allegations, and responsibility established by a court must not be confused.

## 4. Mathematical model

### 4.1. Cumulative harm

Let:

- \(H(t)\) be cumulative established harm.
- \(\lambda(t)\) be the rate of new harm.

Then:

\[
\frac{dH}{dt}=\lambda(t),\qquad \lambda(t)\geq0
\]

\[
H(t)=H(0)+\int_0^t\lambda(\tau)d\tau
\]

Historical harm does not decrease after remorse or punishment.

### 4.2. Outstanding accountability

A separate conceptual variable:

\[
\frac{dA}{dt}=\lambda_A(t)-s(t)-r(t)
\]

where:

- \(\lambda_A\) is newly established responsibility;
- \(s(t)\) is accountability fulfilled through lawful punishment;
- \(r(t)\) is the permissible reduction in outstanding accountability through restorative measures.

The units of measurement, nonnegativity of \(A(t)\), legal constraints, and impossibility of automatically canceling out serious crimes require clarification.

### 4.3. Markov model of behavior

Proposed states:

- \(S_1\) — actively causing harm.
- \(S_2\) — cessation of unlawful acts.
- \(S_3\) — verified cooperation and restorative actions.
- \(S_4\) — sustained desistance from criminal behavior.

Reverse transitions and reoffending are possible.

For a continuous-time Markov process:

\[
\frac{d\mathbf p(t)}{dt}=\mathbf p(t)Q(t)
\]

The transition matrix \(Q(t)\) changes with verified events and new evidence.

### 4.4. Forecast of future harm

\[
R(t)=\int_t^{t+T}\sum_i p_i(\tau)h_i(\tau)d\tau
\]

where \(h_i\) is the expected rate of harm in state \(i\).

Key property:

\[
H(t_2)\geq H(t_1)
\]

while the following is possible:

\[
R(t_2)\ll R(t_1)
\]

Thus, past responsibility remains even when future risk decreases substantially.

### 4.5. Multicriteria decision

The following optimization is proposed for the research model:

\[
a^*(t)=\arg\min_{a\in\mathcal A_{\mathrm{lawful}}}
\left[
w_1L_{\mathrm{future}}(a,t)
+w_2L_{\mathrm{justice}}(a,t)
+w_3L_{\mathrm{rights}}(a,t)
\right]
\]

where \(a\) is a lawful legal measure.

The model must separate responsibility, predicted risk, normative assumptions, and uncertainty.

## 5. Global moral and legal model

The initial idea of limiting the scope to Western legal systems was expanded.

**Decision:** study the legal and moral systems of all humanity, including cultures whose views conflict with the author's personal beliefs.

Do not assume that Western Europe or the United States has a universal monopoly on justice.

At the same time, do not equate a state's laws with the views of every resident.

### Three independent layers

For country \(c\), offense \(x\), and time \(t\):

\[
\mathbf M_c(x,t)=
\begin{bmatrix}
L_c(x,t)\\
J_c(x,t)\\
V_c(x,t)
\end{bmatrix}
\]

- \(L\) — formal legislation.
- \(J\) — actual judicial practice.
- \(V\) — the population's moral views.

### Population weighting

\[
G(x,t)=
\frac{\sum_c P_c(t)V_c(x,t)}
{\sum_c P_c(t)}
\]

where \(P_c(t)\) is the population size.

This is one possible way to define an average public assessment across humanity.

The following should also be compared:

- Equal weight for each country.
- Population weights.
- Mixed systems.
- Estimates accounting for statistical uncertainty.

Country weights should not automatically be equated with moral correctness.

### Go beyond the mean

Also retain:

- The median.
- Variance.
- The distribution of views.
- The degree of polarization.
- Confidence intervals.
- The share of the population without representative data.

Two cultures with the same average assessment may have completely different distributions of views.

## 6. Evolution of morality over time

The model should account for historical changes in attitudes toward crimes and punishments:

\[
\frac{\partial G(x,t)}{\partial t}
\]

Possible research topics:

- Capital punishment.
- Corporal punishment.
- Sexual offenses.
- Domestic violence.
- War crimes.
- Torture.
- Religiously motivated punishments.
- Children's rights.

Compare generations and historical periods as well as countries.

A change in the prevalence of a belief does not itself establish its moral correctness.

## 7. Data sources

Main candidates:

| Source | Purpose |
|---|---|
| [US Sentencing Commission](https://www.ussc.gov/research/datafiles/commission-datafiles) | US federal criminal cases, sentences, offense characteristics |
| [Sentencing Council](https://sentencingcouncil.org.uk/) | England and Wales: sentencing principles, aggravating and mitigating factors |
| [International Criminal Court](https://www.icc-cpi.int/) | International crimes, command responsibility, case law |
| [HUDOC](https://hudoc.echr.coe.int/) | European human rights standards |
| [World Values Survey](https://www.worldvaluessurvey.org/) | Representative surveys of moral and social values |
| [World Justice Project](https://worldjusticeproject.org/rule-of-law-index) | Rule of law, law enforcement |
| [Amnesty International](https://www.amnesty.org/) | Capital punishment and human rights statistics |

Licenses, coverage, comparability across jurisdictions, representativeness, and programmatic data access need to be checked.

## 8. Proposed architecture

```text
Global Moral Atlas
│
├── Data Ingestion
│   ├── Judicial Decisions
│   ├── Criminal Law
│   ├── Moral Surveys
│   ├── Historical Datasets
│   └── Demographics
│
├── Data Normalization
│   ├── Crime Ontology
│   ├── Jurisdiction Mapping
│   ├── Evidence Quality
│   └── Historical Context
│
├── Empirical Models
│   ├── Sentencing Distributions
│   ├── Harm and Culpability
│   ├── Population Weighting
│   └── Cross-Cultural Comparison
│
├── Dynamic Models
│   ├── Cumulative Harm — ODE
│   ├── Outstanding Accountability
│   ├── Markov State Transitions
│   ├── Bayesian Evidence Updates
│   └── Future Risk Forecasting
│
├── Normative Models
│   ├── Retributive Justice
│   ├── Preventive Justice
│   ├── Consequentialism
│   ├── Restorative Justice
│   └── Rights Constraints
│
└── Outputs
    ├── Historical Sentencing Estimate
    ├── Accountability Assessment
    ├── Future Risk Assessment
    ├── Global Moral Distribution
    ├── Uncertainty and Sensitivity
    └── Explainable Legal Policy Analysis
```

## 9. Main methodological problems

1. **Is–ought gap:** the prevalence of a punishment does not imply that it is just.
2. **Historical bias:** judicial systems may be unequal, corrupt, or discriminatory.
3. **Comparability:** identical offense names in different legal systems do not always describe the same acts.
4. **Evidence uncertainty:** the absence of a proven crime does not amount to proven innocence.
5. **Causal inference:** determining whether a particular punishment actually prevented future harm is difficult.
6. **Irreversibility:** a statistical assessment must not automatically authorize irreversible violence.
7. **Aggregation:** a global average assessment may conceal deep polarization.
8. **Political power:** the severity of laws does not always reflect the population's beliefs.
9. **Model calibration:** moral weights must be explicit, adjustable, and subject to sensitivity analysis.

## 10. Decisions already made

- The model should be dynamic rather than a static ranking.
- Use real court cases for empirical calibration.
- Separate historical harm, outstanding accountability, and future risk.
- Combine retribution and prevention.
- Account for new evidence, remorse, cooperation, and behavioral change.
- Use differential equations, Markov models, and Bayesian updating.
- Study all regions of the world, not only Western countries.
- Store legislation, judicial practice, and public beliefs separately.
- Support different global weighting methods.
- Do not conceal disagreements between moral systems.
- Account for changes in morality over historical time.
- Make results explainable, with error estimates and limitations.

## 11. Open questions for the next stage

**A. Mathematics**

How should units of harm, responsibility, and punishment severity be defined? Is a single 0–100 scale needed, or is it better to retain a vector of assessments?

**B. Moral aggregation**

Can a global assessment be obtained without implicitly imposing one culture's values? How can conflicting moral systems be compared?

**C. Normative model**

How should the weights of retribution, prevention, rehabilitation, and restorative justice be defined? Which constraints must remain independent of the optimization result?

**D. Evidence and statistics**

How can real court cases be normalized, different legal systems accounted for, and the causal effects of circumstances distinguished from correlation?

**E. Software implementation**

Which architecture should be chosen for the research prototype? The preliminary candidate is Python, PostgreSQL, and scientific libraries for statistics, ODEs, Markov models, and Bayesian inference.

## 12. Next task

Start with a formal mathematical definition of **crime severity**.

Develop:

1. An ontology of crimes and circumstances.
2. A multidimensional feature vector.
3. An empirical model based on real court cases.
4. A method for calibration across jurisdictions.
5. A method for estimating uncertainty.
6. A dynamic system for accumulating responsibility and updating risk.
7. An initial small computational experiment with synthetic data, followed by real judicial datasets.

**Main research objective:** investigate how far human concepts of culpability and justice can be mathematically formalized using historical data, legal scholarship, statistics, moral philosophy, and dynamical systems theory.

Do not assume in advance that a universal formula for justice exists. Investigate which parts can be objectively measured and which inevitably depend on normative choices.
