import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

processed = Path("data/processed")
reports = Path("reports")

nav = pd.read_csv(processed / "02_nav_history.csv")
funds = pd.read_csv(processed / "01_fund_master.csv")

nav["date"] = pd.to_datetime(nav["date"])
nav = nav.sort_values(["amfi_code", "date"])

nav["daily_return"] = nav.groupby("amfi_code")["nav"].pct_change()

results = []

for code, group in nav.groupby("amfi_code"):

    returns = group["daily_return"].dropna()

    if len(returns) < 30:
        continue

    var95 = np.percentile(returns, 5) * 100
    cvar95 = returns[returns <= np.percentile(returns, 5)].mean() * 100

    results.append({
        "amfi_code": code,
        "VaR_95_pct": var95,
        "CVaR_95_pct": cvar95
    })

var_df = pd.DataFrame(results)

var_df = var_df.merge(
    funds[["amfi_code", "scheme_name", "risk_category"]],
    on="amfi_code",
    how="left"
)

var_df.to_csv(
    reports / "var_cvar_report.csv",
    index=False
)

print("Saved: reports/var_cvar_report.csv")
print(var_df.head())

# Rolling 90-day Sharpe Ratio for 5 key funds
key_funds = [119551, 120503, 118632, 119092, 120841]

rolling_data = nav[nav["amfi_code"].isin(key_funds)].copy()

plt.figure(figsize=(14, 7))

for code, group in rolling_data.groupby("amfi_code"):
    group = group.sort_values("date").copy()

    group["rolling_sharpe"] = (
        group["daily_return"].rolling(90).mean()
        / group["daily_return"].rolling(90).std()
    ) * np.sqrt(252)

    scheme_name = funds.loc[
        funds["amfi_code"] == code, "scheme_name"
    ].values[0][:25]

    plt.plot(group["date"], group["rolling_sharpe"], label=scheme_name)

plt.title("Rolling 90-Day Sharpe Ratio - 5 Key Funds")
plt.xlabel("Date")
plt.ylabel("Rolling Sharpe Ratio")
plt.legend()
plt.tight_layout()

plt.savefig(reports / "rolling_sharpe_chart.png", dpi=300)
plt.close()

print("Saved: reports/rolling_sharpe_chart.png")


# Investor Cohort Analysis
transactions = pd.read_csv(processed / "08_investor_transactions.csv")
transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"])

transactions["transaction_year"] = transactions["transaction_date"].dt.year

first_year = transactions.groupby("investor_id")["transaction_year"].min().reset_index()
first_year.columns = ["investor_id", "cohort_year"]

transactions = transactions.merge(first_year, on="investor_id", how="left")

sip_transactions = transactions[transactions["transaction_type"] == "SIP"]

cohort_analysis = sip_transactions.groupby("cohort_year").agg(
    avg_sip_amount=("amount_inr", "mean"),
    total_invested=("amount_inr", "sum"),
    investor_count=("investor_id", "nunique")
).reset_index()

cohort_analysis.to_csv(reports / "cohort_analysis.csv", index=False)

print("Saved: reports/cohort_analysis.csv")


# SIP Continuity Analysis
sip_sorted = sip_transactions.sort_values(["investor_id", "transaction_date"])

sip_counts = sip_sorted.groupby("investor_id").size()
eligible_investors = sip_counts[sip_counts >= 6].index

sip_eligible = sip_sorted[sip_sorted["investor_id"].isin(eligible_investors)].copy()

sip_eligible["gap_days"] = sip_eligible.groupby("investor_id")["transaction_date"].diff().dt.days

sip_continuity = sip_eligible.groupby("investor_id").agg(
    avg_gap_days=("gap_days", "mean"),
    sip_count=("transaction_date", "count"),
    total_sip_amount=("amount_inr", "sum")
).reset_index()

sip_continuity["risk_status"] = np.where(
    sip_continuity["avg_gap_days"] > 35,
    "At-risk",
    "Regular"
)

sip_continuity.to_csv(reports / "sip_continuity.csv", index=False)

print("Saved: reports/sip_continuity.csv")