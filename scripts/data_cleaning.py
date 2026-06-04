import pandas as pd
from pathlib import Path

raw_path = Path("data/raw")
processed_path = Path("data/processed")

processed_path.mkdir(exist_ok=True)

# -------------------------
# 02 NAV HISTORY
# -------------------------
nav = pd.read_csv(raw_path / "02_nav_history.csv")

nav["date"] = pd.to_datetime(nav["date"])
nav = nav.sort_values(["amfi_code", "date"])

nav = nav.drop_duplicates()

nav["nav"] = nav.groupby("amfi_code")["nav"].ffill()

nav = nav[nav["nav"] > 0]

nav.to_csv(processed_path / "02_nav_history.csv", index=False)

print("✓ NAV History cleaned")


# -------------------------
# 07 SCHEME PERFORMANCE
# -------------------------
perf = pd.read_csv(raw_path / "07_scheme_performance.csv")

return_cols = [
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct",
    "benchmark_3yr_pct"
]

for col in return_cols:
    perf[col] = pd.to_numeric(perf[col], errors="coerce")

expense_anomalies = perf[
    (perf["expense_ratio_pct"] < 0.1)
    | (perf["expense_ratio_pct"] > 2.5)
]

print("\nExpense Ratio Anomalies:")
print(len(expense_anomalies))

perf.to_csv(processed_path / "07_scheme_performance.csv", index=False)

print("✓ Scheme Performance cleaned")


# -------------------------
# 08 INVESTOR TRANSACTIONS
# -------------------------
txn = pd.read_csv(raw_path / "08_investor_transactions.csv")

txn["transaction_date"] = pd.to_datetime(txn["transaction_date"])

txn["transaction_type"] = (
    txn["transaction_type"]
    .str.strip()
    .str.title()
)

txn = txn[
    txn["transaction_type"].isin(
        ["Sip", "Lumpsum", "Redemption"]
    )
]

txn = txn[txn["amount_inr"] > 0]

valid_kyc = ["Verified", "Pending", "Rejected"]

invalid_kyc = txn[
    ~txn["kyc_status"].isin(valid_kyc)
]

print("\nInvalid KYC Records:")
print(len(invalid_kyc))

txn.to_csv(
    processed_path / "08_investor_transactions.csv",
    index=False
)

print("✓ Investor Transactions cleaned")