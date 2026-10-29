
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
RESULTS_PATH = DATA_DIR / "results.json"
METRICS_PATH = DATA_DIR / "smoke_metrics.json"


# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="NCM-SpeedLab",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# Styling
# --------------------------------------------------
st.markdown(
    """
    <style>
    /* Main page spacing */
    .stApp {
        overflow-x: hidden;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 3rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* Hero banner */
    .hero {
        box-sizing: border-box;
        width: 100%;
        padding: 1.75rem 1.8rem;
        margin: 0 0 1.75rem 0;
        border: 1px solid rgba(128, 128, 128, 0.28);
        border-radius: 16px;
        overflow-wrap: anywhere;
    }

    .hero-kicker {
        display: block;
        margin: 0 0 0.55rem 0;
        padding: 0;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.13em;
        line-height: 1.6;
        text-transform: uppercase;
        opacity: 0.75;
    }

    .hero-title {
        margin: 0 0 0.65rem 0;
        padding: 0;
        font-size: clamp(1.8rem, 4vw, 2.6rem);
        font-weight: 750;
        line-height: 1.2;
        overflow-wrap: anywhere;
    }

    .hero-title span {
        display: inline-block;
        margin-left: 0.15rem;
    }

    .hero-sub {
        max-width: 950px;
        margin: 0;
        font-size: 1rem;
        line-height: 1.65;
        opacity: 0.82;
    }

    /* General typography */
    h1, h2, h3 {
        scroll-margin-top: 2rem;
    }

    .small-note {
        font-size: 0.85rem;
        line-height: 1.5;
        opacity: 0.8;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        padding: 1rem;
        border: 1px solid rgba(128, 128, 128, 0.22);
        border-radius: 12px;
        min-height: 115px;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
    }

    [data-testid="stMetricValue"] {
        font-size: clamp(1.5rem, 2.5vw, 2rem);
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .block-container {
            padding-top: 1.5rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero {
            padding: 1.2rem;
            border-radius: 12px;
        }

        .hero-kicker {
            font-size: 0.68rem;
            letter-spacing: 0.09em;
        }

        .hero-sub {
            font-size: 0.93rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Hero section
# --------------------------------------------------
st.markdown(
    """
    <section class="hero">
        <div class="hero-kicker">
            Research prototype · NCM · XSum
        </div>
        <div class="hero-title">
            NCM-SpeedLab <span>⚡</span>
        </div>
        <p class="hero-sub">
            Explore real Next-Concept Modeling evaluation outputs,
            inspect summaries, and keep benchmark claims reproducible.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Data loading
# --------------------------------------------------
def load_json(path: Path) -> Any | None:
    """Load a JSON file safely."""
    if not path.exists():
        return None

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        st.error(f"Could not read {path.name}: {exc}")
        return None


metrics_data = load_json(METRICS_PATH)
metrics = metrics_data if isinstance(metrics_data, dict) else {}

records_data = load_json(RESULTS_PATH)
records = records_data if isinstance(records_data, list) else []

# Keep only dictionary records so malformed entries do not crash the UI.
records = [record for record in records if isinstance(record, dict)]


# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:
    st.header("Project status")

    st.success("Official NCM checkpoint evaluated")

    st.caption("Smoke test only · 4 examples")

    st.divider()

    st.subheader("About this prototype")

    st.write(
        "This dashboard displays saved outputs from the official "
        "NCM evaluation pipeline. It does not run new model inference "
        "from arbitrary text yet."
    )

    st.divider()

    st.subheader("Data files")

    st.write(
        "Expected files:"
    )

    st.code(
        "data/\n"
        "├── smoke_metrics.json\n"
        "└── results.json",
        language="text",
    )


# --------------------------------------------------
# Data validation and metadata
# --------------------------------------------------
if not metrics:
    st.warning(
        "The benchmark metadata file "
        "`data/smoke_metrics.json` is missing or empty."
    )

if not records:
    st.info(
        "No saved examples found yet. Download `results.json` "
        "from your Colab evaluation and place it at "
        "`NCM-SpeedLab/data/results.json`."
    )


def numeric_metric(key: str) -> float | None:
    """Return a valid numeric metric, excluding booleans."""
    value = metrics.get(key)

    if isinstance(value, bool):
        return None

    if isinstance(value, (int, float)):
        return float(value)

    return None


n_examples = metrics.get("examples", len(records))

try:
    n_examples = int(n_examples)
except (TypeError, ValueError):
    n_examples = len(records)

rouge1 = numeric_metric("rouge1")
rouge2 = numeric_metric("rouge2")
rougeL = numeric_metric("rougeL")
gen_ppl = numeric_metric("genPPL")


# --------------------------------------------------
# Evaluation overview
# --------------------------------------------------
st.header("Evaluation overview")

metric_columns = st.columns(4)


def format_metric(value: float | None) -> str:
    return f"{value:.2f}" if value is not None else "—"


metric_values = [
    ("ROUGE-1", rouge1),
    ("ROUGE-2", rouge2),
    ("ROUGE-L", rougeL),
    ("Generation PPL", gen_ppl),
]

for column, (label, value) in zip(metric_columns, metric_values):
    column.metric(label, format_metric(value))


st.caption(
    f"Task: {metrics.get('task', 'XSum summarization')} · "
    f"Examples: {len(records) if records else n_examples} · "
    f"Model: {metrics.get('model', 'Official HazyResearch NCM checkpoint')}"
)


st.warning(
    "Interpretation limit: these scores come from a four-example "
    "smoke test. They verify that the evaluation pipeline runs, "
    "but they are not reliable estimates of full-dataset quality. "
    "Generation latency has not been measured, so this dashboard "
    "does not claim an NCM speedup."
)


# --------------------------------------------------
# Main tabs
# --------------------------------------------------
tab_overview, tab_examples, tab_method = st.tabs(
    [
        "Overview",
        "Summary inspection",
        "Method & limitations",
    ]
)


# --------------------------------------------------
# Tab 1: Overview
# --------------------------------------------------
with tab_overview:
    left, right = st.columns([1.1, 1], gap="large")

    with left:
        st.subheader("Quality metrics")

        metric_rows = []

        for name, value in [
            ("ROUGE-1", rouge1),
            ("ROUGE-2", rouge2),
            ("ROUGE-L", rougeL),
        ]:
            if value is not None:
                metric_rows.append(
                    {
                        "Metric": name,
                        "Score": value,
                    }
                )

        if metric_rows:
            chart_data = pd.DataFrame(metric_rows)

            st.bar_chart(
                chart_data,
                x="Metric",
                y="Score",
                horizontal=True,
                height=300,
                use_container_width=True,
            )

            st.caption(
                "ROUGE scores measure lexical overlap with reference "
                "summaries. They do not fully measure factual accuracy "
                "or summary usefulness."
            )
        else:
            st.info(
                "Metric values will appear when valid values are "
                "available in smoke_metrics.json."
            )

    with right:
        st.subheader("Run metadata")

        metadata = {
            "Evaluation type": metrics.get(
                "evaluation_type", "Smoke test"
            ),
            "Dataset/task": metrics.get(
                "task", "XSum summarization"
            ),
            "Examples evaluated": (
                len(records) if records else n_examples
            ),
            "Average output words": metrics.get(
                "avg_output_words", "Not recorded"
            ),
            "Hardware": metrics.get(
                "hardware",
                "Google Colab GPU — verify exact GPU model",
            ),
        }

        for label, value in metadata.items():
            st.markdown(f"**{label}:** {value}")

        st.divider()

        st.subheader("Next milestone")

        st.write(
            "Run a larger reproducible evaluation, record end-to-end "
            "latency, and compare against an appropriate autoregressive "
            "baseline under controlled conditions."
        )


# --------------------------------------------------
# Tab 2: Generated and reference summaries
# --------------------------------------------------
with tab_examples:
    st.subheader("Compare generated output with the reference")

    if records:
        query = st.text_input(
            "Filter examples",
            placeholder="Search generated or reference summaries",
            key="summary_filter",
        )

        filtered = []

        for position, record in enumerate(records, start=1):
            generated = str(record.get("ncm_summary", ""))
            reference = str(record.get("reference_summary", ""))

            searchable_text = f"{generated} {reference}"

            if (
                not query
                or query.casefold() in searchable_text.casefold()
            ):
                filtered.append(
                    (
                        position,
                        record,
                        generated,
                        reference,
                    )
                )

        st.caption(
            f"Showing {len(filtered)} of {len(records)} examples"
        )

        for position, record, generated, reference in filtered:
            example_id = record.get("example_id", position)

            with st.expander(
                f"Example {position} · dataset ID {example_id}",
                expanded=False,
            ):
                col_a, col_b = st.columns(2, gap="large")

                with col_a:
                    st.markdown("**NCM-generated summary**")
                    st.write(generated or "(empty output)")

                with col_b:
                    st.markdown("**Reference summary**")
                    st.write(reference or "(empty reference)")

                st.caption(
                    "Review factual consistency and key-detail "
                    "coverage—not word overlap alone."
                )

        if filtered:
            export_rows = [
                {
                    "example_id": record.get("example_id", position),
                    "ncm_summary": generated,
                    "reference_summary": reference,
                }
                for position, record, generated, reference in filtered
            ]

            st.download_button(
                label="Download filtered examples as JSON",
                data=json.dumps(
                    export_rows,
                    indent=2,
                    ensure_ascii=False,
                ),
                file_name="ncm_speedlab_filtered_results.json",
                mime="application/json",
            )

        elif query:
            st.info(
                "No examples match that search. Try a different keyword."
            )

    else:
        st.info(
            "Add data/results.json to enable generated-versus-reference "
            "inspection."
        )


# --------------------------------------------------
# Tab 3: Methodology and limitations
# --------------------------------------------------
with tab_method:
    st.subheader("What this version demonstrates")

    st.markdown(
        """
        - Uses outputs saved by the official NCM evaluation script.
        - Displays the recorded XSum ROUGE and generation-perplexity metrics.
        - Supports side-by-side inspection of generated and reference summaries.
        - Makes the small smoke-test limitation visible.
        """
    )

    st.subheader("What it does not demonstrate yet")

    st.markdown(
        """
        - It is not a general-purpose NCM chatbot or arbitrary-input summarizer.
        - The four-example score is not a full XSum benchmark result.
        - No latency comparison or speedup is reported.
        - No claim is made that NCM outperforms GPT, Claude, or all LLMs.
        """
    )

    st.subheader("Reproducibility checklist")

    st.checkbox(
        "Record exact Colab GPU model and runtime",
        key="check_gpu",
    )

    st.checkbox(
        "Save the evaluation command and model/config revision",
        key="check_revision",
    )

    st.checkbox(
        "Run a larger test and retain the full output artifact",
        key="check_larger_test",
    )

    st.checkbox(
        "Benchmark a suitable autoregressive baseline under matched conditions",
        key="check_baseline",
    )


# --------------------------------------------------
# Footer
# --------------------------------------------------
st.divider()

st.caption(
    "NCM-SpeedLab · Portfolio research prototype · "
    "Based on saved outputs from the official HazyResearch/NCM evaluation pipeline."
)
