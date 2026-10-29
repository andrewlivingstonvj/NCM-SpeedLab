# NCM-SpeedLab

A portfolio research dashboard for inspecting outputs from the official HazyResearch Next-Concept Modeling (NCM) XSum evaluation.

## Current status

- Official NCM evaluation completed on 4 XSum examples in Google Colab.
- Saved metrics: ROUGE-1 42.96, ROUGE-2 13.99, ROUGE-L 36.60, generation perplexity 37.46.
- These values are from a four-example smoke test only. They are not a reliable full benchmark result.
- This dashboard displays saved outputs; it does not yet run NCM on arbitrary user text.
- Generation latency has not been measured and no speedup claim is made.

## Setup on Windows PowerShell

Activate your existing virtual environment, then from this directory run:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Add your Colab outputs

Download `results.json` from `/content/ncm/eval/xsum_smoke/results.json` in Colab and place it at:

```text
data/results.json
```

The JSON should be a list of objects containing `example_id`, `ncm_summary`, and `reference_summary`. The dashboard reads `data/smoke_metrics.json` for the four-example smoke-test metrics.

## Next research milestones

1. Record the exact GPU model and repository/config revision.
2. Run a larger, reproducible XSum evaluation.
3. Measure latency with a documented timing protocol.
4. Compare with a suitable autoregressive baseline under controlled conditions.
5. Only then report a quality/speed trade-off.

## Source

- Official implementation: https://github.com/HazyResearch/ncm
- Research paper: https://arxiv.org/abs/2610.14162
