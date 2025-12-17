"""Toy Streamlit app students can customize for STAT 386 projects."""

from __future__ import annotations

import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

import pandas as pd
import streamlit as st

# Allow running via `streamlit run src/NEO_Nature/streamlit_app.py` without
# requiring an installed package.
SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from NEO_Nature.analysis import run_analysis_pipeline
from NEO_Nature.cleaning import run_cleaning_pipeline


def _sample_data() -> pd.DataFrame:
    path = Path("data/merged_neo_disaster_data.csv")
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    return df.head(10)


def _run_with_capture(func) -> str:
    """Capture stdout from placeholder pipelines so Streamlit can display it."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        func()
    return buffer.getvalue().strip()


def main() -> None:
    st.set_page_config(page_title="STAT 386 Final Project", layout="wide")
    st.title("STAT 386 Final Project")
    st.write(
        "Use this template Streamlit app as a quick sandbox. Replace the sample data, "
        "plug in your cleaning pipeline, and surface the most important visuals for your final deliverable."
    )

    with st.sidebar:
        st.header("Controls")
        dataset_choice = st.selectbox("Dataset", ["Sample Data", "Upload CSV"])
        show_cleaning = st.checkbox("Preview cleaning pipeline output")
        show_analysis = st.checkbox("Preview analysis pipeline output")

    if dataset_choice == "Sample Data":
        if not Path("data/merged_neo_disaster_data.csv").exists():
            st.warning(
                "Missing `data/merged_neo_disaster_data.csv`. "
                "Run the cleaning pipeline first (or enable the cleaning checkbox)."
            )
        df = _sample_data()
    else:
        uploaded = st.file_uploader("Upload a CSV file", type="csv")
        if uploaded:
            df = pd.read_csv(uploaded)
        else:
            st.info("No file uploaded yet. Falling back to the sample data so the widgets stay live.")
            df = _sample_data()

    st.subheader("Data Preview")
    st.dataframe(df, use_container_width=True)
    

    if show_cleaning:
        st.subheader("Cleaning Pipeline Output")
        cleaning_output = _run_with_capture(run_cleaning_pipeline)
        st.code(cleaning_output or "run_cleaning_pipeline() did not emit text.")
        st.caption("Replace run_cleaning_pipeline with your real preprocessing logic.")

    if show_analysis:
        st.subheader("Analysis Pipeline Output")
        analysis_output = _run_with_capture(run_analysis_pipeline)
        st.code(analysis_output or "run_analysis_pipeline() did not emit text.")
        st.caption("Swap this stub with charts, metrics, or model diagnostics from your project.")

    st.info(
        "Next steps: customize the sidebar controls, drop in Streamlit charts (st.bar_chart, st.map, etc.), "
        "and layer in explanations so stakeholders can self-serve results."
    )


if __name__ == "__main__":
    main()
