import pandas as pd

scorecard = pd.read_csv("reports/fund_scorecard.csv")
funds = pd.read_csv("data/processed/01_fund_master.csv")

df = scorecard.merge(
    funds[["amfi_code", "risk_category"]],
    on="amfi_code",
    how="left"
)

risk_map = {
    "Low": ["Low"],
    "Moderate": ["Moderate", "Moderately High"],
    "High": ["High", "Very High"]
}

risk_appetite = input("Enter Risk Appetite (Low/Moderate/High): ")

filtered = df[df["risk_category"].isin(risk_map[risk_appetite])]

top3 = filtered.sort_values(
    "sharpe_ratio",
    ascending=False
).head(3)

print("\nRecommended Funds:\n")

print(
    top3[
        [
            "scheme_name",
            "risk_category",
            "sharpe_ratio",
            "final_score"
        ]
    ]
)