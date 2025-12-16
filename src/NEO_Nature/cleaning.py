# packages
import pandas as pd

def run_cleaning_pipeline():
    print("Running cleaning pipeline...")

    # Load NEO and disaster datasets
    neo_data = pd.read_csv("neo_data.csv")
    disaster_data = pd.read_csv("disaster_data.csv")

    # Merge on the 'date' column
    merged = pd.merge(
        disaster_data,
        neo_data,
        on="date",
        how="left"
    )
    
    # Remove rows with NA values
    merged = merged.dropna()
    print("removing NA values...")

    #converting date column to datetime format
    merged['date'] = pd.to_datetime(merged['date'])
    print("converting date column to datetime format...")

    # save merged/cleaned file
    merged.to_csv("merged_neo_disaster_data.csv", index=False)

    print("Merged dataset created and saved at NEO-Nature/merged_neo_disaster_data.csv")


