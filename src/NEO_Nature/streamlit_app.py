"""Toy Streamlit app students can customize for STAT 386 projects."""

from __future__ import annotations

import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

import pandas as pd
import streamlit as st

from NEO_Nature.analysis import run_analysis_pipeline
from NEO_Nature.cleaning import run_cleaning_pipeline


def _sample_data() -> pd.DataFrame:
    df = pd.read_csv("data/merged_neo_disaster_data.csv")
    return df


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

    df = _sample_data()
    df["date"] = pd.to_datetime(df["date"])

    with st.sidebar:
        st.header("Controls")
        show_cleaning = st.checkbox("Preview cleaning pipeline output")
        show_analysis = st.checkbox("Preview analysis pipeline output")
        min_diameter = st.slider(
        "Minimum asteroid diameter (km)",
        min_value=0.0,
        max_value=1.0,
        value=0.3,
        step=0.05
        )

        start_date, end_date = st.date_input(
            "Date range",
            value=(df["date"].min(), df["date"].max())
        )

        filtered_df = df[
        (df["estimated_diameter_max_km"] >= min_diameter) &
        (df["date"] >= pd.to_datetime(start_date)) &
        (df["date"] <= pd.to_datetime(end_date))
        ]    

    st.subheader("Data Preview")
    st.dataframe(filtered_df, use_container_width=True)



    if show_cleaning:
        st.subheader("Cleaning Pipeline Output")
        cleaning_output = _run_with_capture(run_cleaning_pipeline)
        st.code(cleaning_output or "run_cleaning_pipeline() did not emit text.")
        st.caption("Replace run_cleaning_pipeline with your real preprocessing logic.")

    if show_analysis:
        st.subheader("Analysis Pipeline Output")
        analysis_output = _run_with_capture(run_analysis_pipeline)
        st.code(analysis_output or "run_analysis_pipeline() did not emit text.")
        st.pyplot(run_analysis_pipeline())
        st.caption("There does not appear to be a relationship between asteroid size and disaster count.")

    st.subheader("Natural Disasters and Asteroids Per Year")

    ast = pd.read_csv("data/neo_data.csv")
    dia = pd.read_csv("data/disaster_data.csv")

    ast['date'] = pd.to_datetime(ast['date'])
    dia['date'] = pd.to_datetime(dia['date'])

    yearly_dia = dia[
        (dia["date"] >= pd.to_datetime(start_date)) &
        (dia["date"] <= pd.to_datetime(end_date))
        ]  
    
    yearly_dia["year"] = yearly_dia["date"].dt.year
    
    yearly_ast = ast[
        (ast["estimated_diameter_max_km"] >= min_diameter) &
        (ast["date"] >= pd.to_datetime(start_date)) &
        (ast["date"] <= pd.to_datetime(end_date))
        ]  
    
    yearly_ast["year"] = yearly_ast["date"].dt.year

    disasters_per_year = yearly_dia.groupby("year").size().rename("Disasters")
    asteroids_per_year = (yearly_ast.dropna(subset=["estimated_diameter_max_km"]).groupby("year").size().rename("Asteroids"))
    
    bar_df = pd.concat(
        [disasters_per_year, asteroids_per_year],
        axis=1
    ).fillna(0)


    st.bar_chart(bar_df)
    st.caption(
        "As the amount of natural disasters increases over the years, the number of detected asteroids does not appear to follow the same trend."
    )

    st.subheader("Asteroid Size vs Disaster Count")

    scatter_df = (
        filtered_df
        .groupby("date")
        .agg(
            max_diameter_km=("estimated_diameter_max_km", "max"),
            disaster_count=("disaster_type", "count")
        )
        .reset_index()
    )

    st.scatter_chart(
        scatter_df,
        x="max_diameter_km",
        y="disaster_count"
    )
    st.caption(
        "Each point represents a single day. No clear relationship is visible between asteroid size and the number of natural disasters."
    )


if __name__ == "__main__":
    main()
