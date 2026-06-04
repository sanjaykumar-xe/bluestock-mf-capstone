import pandas as pd

df = pd.read_csv("data/processed/02_nav_history.csv")

print("Rows:", len(df))

print("\nMissing NAV values:")
print(df["nav"].isnull().sum())

print("\nNAV <= 0:")
print((df["nav"] <= 0).sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())