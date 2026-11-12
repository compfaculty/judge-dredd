# Research notebooks

[Theory and Mathematics Laboratory](theory_and_math.ipynb) is an interactive,
English-language presentation of the project's research boundaries and mathematics.
It uses the existing mathematical utilities and bundled case resources. It includes
Bradley–Terry comparisons, synthetic feature-weight sensitivity, exact integration
of a synthetic harm rate, and an evidence annotation explorer with source pinpoints.

## Run

From the project root:

```bash
source .venv/bin/activate
pip install -e '.[dev,notebook]'
jupyter lab notebooks/theory_and_math.ipynb
```

Choose the virtual environment's Python kernel and run all cells in order. Sliders
update when released. The notebook renders defaults separately so static readers can
see plots without widgets. Restart and run all cells to restore the defaults.

If Jupyter runs outside this environment, register this environment's kernel:

```bash
python -m ipykernel install --user --name judge-dredd --display-name 'Judge Dredd'
```

Then select **Judge Dredd** in Jupyter. The notebook imports the installed package,
so it works from either the project root or the notebook directory.

## Verify and export

Execute in a fresh kernel, retaining the source notebook unchanged:

```bash
jupyter nbconvert --to notebook --execute notebooks/theory_and_math.ipynb \
  --output theory_and_math.executed --output-dir /tmp \
  --ExecutePreprocessor.timeout=120
pytest -q
```

Export that executed notebook for sharing:

```bash
jupyter nbconvert --to html /tmp/theory_and_math.executed.ipynb --output-dir /tmp
```

HTML exports show default plots and saved output; Python callbacks require a live
kernel. They are not standalone interactive web applications. The source notebook is
delivered without execution output to keep it small and avoid committing widget state.

## Interpretation and provenance

All numeric experiments use invented inputs and explicitly stated units and baselines.
The evidence explorer reads the bundled case JSON and verifies the bundled PDF hash;
it neither alters the frozen assessment nor writes human reviews. Curated annotations
still require primary-source verification. The notebook is not a blinded case experiment.

No scientific validation, calibrated MSU, real-case guilt probability, sentencing, or
individual risk prediction is claimed. Outstanding accountability remains unimplemented;
the mathematical audit's production-prediction restrictions remain in force. Independent
scientific review is pending. See [MATH_AUDIT.md](../docs/MATH_AUDIT.md).
