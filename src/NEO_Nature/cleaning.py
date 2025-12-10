# packages
import pandas as pd

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
    
    # save merged/cleaned file
    merged.to_csv("data/merged_neo_disaster_data.csv", index=False)

    print("Merged dataset created and saved at data/merged_neo_disaster_data.csv")

if __name__ == "__main__":
    run_cleaning_pipeline()
