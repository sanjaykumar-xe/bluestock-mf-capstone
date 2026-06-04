import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

# Create database
engine = create_engine("sqlite:///db/bluestock_mf.db")

processed_path = Path("data/processed")

files = [
    "01_fund_master.csv",
    "02_nav_history.csv",
    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "07_scheme_performance.csv",
    "08_investor_transactions.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv"
]

for file in files:
    df = pd.read_csv(processed_path / file)

    table_name = file.replace(".csv", "")

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    print(f"{table_name}: {len(df)} rows loaded")

print("\nDatabase created successfully.")