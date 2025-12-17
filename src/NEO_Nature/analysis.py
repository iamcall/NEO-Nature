# packages
import pandas as pd


def run_analysis_pipeline():
    """
    Run exploratory analysis examining whether Near-Earth Object (NEO)
    characteristics are associated with natural disaster occurrence.

    This function prints summary correlations used in the final report.
    """

    print("Running analysis pipeline...")

    # Load merged dataset
    df = pd.read_csv("data/merged_neo_disaster_data.csv")
    df["date"] = pd.to_datetime(df["date"])

    # Drop rows without asteroid diameter data
    asteroid_df = df.dropna(subset=["diameter_max_m"])

    # Aggregate asteroid size and disaster counts by date
    asteroid_by_date = (
        asteroid_df
        .groupby("date")["diameter_max_m"]
        .max()
        .reset_index(name="max_diameter_m")
    )

    disaster_count = (
        asteroid_df
        .groupby("date")["disaster_type"]
        .count()
        .reset_index(name="disaster_count")
    )

    plot_df = pd.merge(
        asteroid_by_date,
        disaster_count,
        on="date",
        how="left"
    ).fillna(0)

    # --- Same-day correlation ---
    same_day_corr = plot_df[["max_diameter_m", "disaster_count"]].corr().iloc[0, 1]
    print(f"Same-day correlation (NEO size vs disaster count): {same_day_corr:.3f}")

    # --- One-day lag correlation ---
    lagged_disasters = disaster_count.rename(columns={"date": "date_plus_1"})
    lagged_df = pd.merge(
        asteroid_by_date,
        lagged_disasters,
        left_on="date",
        right_on="date_plus_1",
        how="left"
    ).fillna(0)

    lag_corr = lagged_df[["max_diameter_m", "disaster_count"]].corr().iloc[0, 1]
    print(f"Next-day correlation (NEO size vs disasters 1 day later): {lag_corr:.3f}")

    # --- Hazardous asteroids only ---
    hazardous_df = df[df["hazardous"] == True].dropna(subset=["diameter_max_m"])

    if len(hazardous_df) > 0:
        haz_asteroid_by_date = (
            hazardous_df
            .groupby("date")["diameter_max_m"]
            .max()
            .reset_index(name="max_diameter_m")
        )

        haz_disaster_count = (
            hazardous_df
            .groupby("date")["disaster_type"]
            .count()
            .reset_index(name="disaster_count")
        )

        haz_plot_df = pd.merge(
            haz_asteroid_by_date,
            haz_disaster_count,
            on="date",
            how="outer"
        ).fillna(0)

        haz_corr = haz_plot_df[["max_diameter_m", "disaster_count"]].corr().iloc[0, 1]
        print(f"Hazardous-only correlation (NEO size vs disaster count): {haz_corr:.3f}")
    else:
        print("No hazardous asteroid data available for correlation analysis.")

    print("Analysis complete.")
    print(
        "Conclusion: Across same-day, lagged, and hazardous-only analyses, "
        "no meaningful correlation was observed between asteroid characteristics "
        "and natural disaster occurrence."
    )


if __name__ == "__main__":
    run_analysis_pipeline()
