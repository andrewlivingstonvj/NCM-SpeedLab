# Evaluation data

Place the official evaluation export from Colab at `data/results.json`.

The expected structure is a JSON list containing objects with:
- `example_id`
- `ncm_summary`
- `reference_summary`

The `smoke_metrics.json` file contains the metrics from the four-example smoke test. Keep the smoke-test limitation visible and do not present these figures as a full benchmark result.
