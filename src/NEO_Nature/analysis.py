import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run_analysis_pipeline():
    print("Creating Graph...")
    merged_df = pd.read_csv("merged_neo_disaster_data.csv")

    LARGE_DIAMETER_THRESHOLD = 300  

    asteroid_df = merged_df.dropna(subset=["estimated_diameter_max_km"])

    disaster_count = asteroid_df.groupby("date")['disaster_type'].count().reset_index()
    disaster_count.rename(columns={"disaster_type": "disaster_count"}, inplace=True)

    asteroid_by_date = asteroid_df.groupby("date")['estimated_diameter_max_km'].max().reset_index()
    asteroid_by_date.rename(columns={"estimated_diameter_max_km": "max_diameter_km"}, inplace=True)

    plot_df = pd.merge(asteroid_by_date, disaster_count, on="date", how="left")
    plot_df["disaster_count"] = plot_df["disaster_count"].fillna(0)

    plot_df["large_neo"] = plot_df["max_diameter_km"] > LARGE_DIAMETER_THRESHOLD

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        data=plot_df,
        x="max_diameter_km",
        y="disaster_count",
        hue="large_neo",
        style="large_neo",
        s=100,
        ax=ax
    )

    ax.set_title("Asteroid Size vs. Number of Natural Disasters That Day")
    ax.set_xlabel("Largest Asteroid Diameter on Date (m)")
    ax.set_ylabel("Count of Natural Disasters")
    ax.legend(title="Large NEO (>300m)")

    return fig
    
