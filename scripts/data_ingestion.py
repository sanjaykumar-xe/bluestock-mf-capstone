import pandas as pd
import os

DATA_PATH = "data/raw"

csv_files = [f for f in os.listdir(DATA_PATH) if f.endswith(".csv")]

print(f"\nFound {len(csv_files)} CSV files\n")

for file in csv_files:
    file_path = os.path.join(DATA_PATH, file)

    try:
        df = pd.read_csv(file_path)

        print("=" * 60)
        print(f"FILE: {file}")
        print("=" * 60)

        print("Shape:", df.shape)

        print("\nColumns:")
        print(df.columns.tolist())

        print("\nData Types:")
        print(df.dtypes)

        print("\nMissing Values:")
        print(df.isnull().sum())

        print("\nDuplicate Rows:")
        print(df.duplicated().sum())

        print("\nFirst 5 Rows:")
        print(df.head())

    except Exception as e:
        print(f"Error reading {file}: {e}")