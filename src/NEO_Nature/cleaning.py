# packages
import pandas as pd


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "estimated_diameter_max_km" in df.columns and "diameter_max_m" not in df.columns:
        df["diameter_max_m"] = df["estimated_diameter_max_km"] * 1000
    if "estimated_diameter_min_km" in df.columns and "diameter_min_m" not in df.columns:
        df["diameter_min_m"] = df["estimated_diameter_min_km"] * 1000
    if "is_hazardous" in df.columns and "hazardous" not in df.columns:
        df["hazardous"] = df["is_hazardous"].astype("boolean")
    return df


def run_cleaning_pipeline():
    print("Running cleaning pipeline...")

    # Load NEO and disaster datasets
    neo_data = pd.read_csv("data/neo_data.csv")
    disaster_data = pd.read_csv("data/disaster_data.csv")

    # Merge on the 'date' column
    merged = pd.merge(
        disaster_data,
        neo_data,
        on="date",
        how="left"
    )

    merged = _normalize_columns(merged)
    
    # Remove rows with NA values
    merged = merged.dropna()
    print("removing NA values...")

    #converting date column to datetime format
    merged['date'] = pd.to_datetime(merged['date'])
    print("converting date column to datetime format...")

    # save merged/cleaned file
    merged.to_csv("data/merged_neo_disaster_data.csv", index=False)

    print("Merged dataset created and saved at NEO-Nature/data/merged_neo_disaster_data.csv")


