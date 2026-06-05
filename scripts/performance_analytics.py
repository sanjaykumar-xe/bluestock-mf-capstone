import pandas as pd
import numpy as np
from scipy.stats import linregress
from pathlib import Path
import matplotlib.pyplot as plt

processed = Path("data/processed")
reports = Path("reports")
reports.mkdir(exist_ok=True)

nav = pd.read_csv(processed / "02_nav_history.csv")
funds = pd.read_csv(processed / "01_fund_master.csv")
bench = pd.read_csv(processed / "10_benchmark_indices.csv")
perf = pd.read_csv(processed / "07_scheme_performance.csv")

nav["date"] = pd.to_datetime(nav["date"])
bench["date"] = pd.to_datetime(bench["date"])

nav = nav.sort_values(["amfi_code", "date"])

# Daily returns
nav["daily_return"] = nav.groupby("amfi_code")["nav"].pct_change()

# CAGR function
def calculate_cagr(group, years):
    group = group.dropna().sort_values("date")
    end_date = group["date"].max()
    start_date = end_date - pd.DateOffset(years=years)

    period = group[group["date"] >= start_date]

    if len(period) < 2:
        return np.nan

    nav_start = period.iloc[0]["nav"]
    nav_end = period.iloc[-1]["nav"]

    return ((nav_end / nav_start) ** (1 / years) - 1) * 100

results = []

rf_daily = 0.065 / 252

nifty100 = bench[bench["index_name"] == "NIFTY100"].copy()
nifty100 = nifty100.sort_values("date")
nifty100["benchmark_return"] = nifty100["close_value"].pct_change()

for code, group in nav.groupby("amfi_code"):
    group = group.dropna(subset=["daily_return"]).copy()

    avg_daily_return = group["daily_return"].mean()
    std_daily_return = group["daily_return"].std()

    sharpe = ((avg_daily_return - rf_daily) / std_daily_return) * np.sqrt(252) if std_daily_return != 0 else np.nan

    downside = group[group["daily_return"] < 0]["daily_return"].std()
    sortino = ((avg_daily_return - rf_daily) / downside) * np.sqrt(252) if downside != 0 else np.nan

    group["running_max"] = group["nav"].cummax()
    group["drawdown"] = group["nav"] / group["running_max"] - 1
    max_drawdown = group["drawdown"].min() * 100
    max_drawdown_date = group.loc[group["drawdown"].idxmin(), "date"]

    merged = pd.merge(
        group[["date", "daily_return"]],
        nifty100[["date", "benchmark_return"]],
        on="date",
        how="inner"
    ).dropna()

    if len(merged) > 10:
        reg = linregress(merged["benchmark_return"], merged["daily_return"])
        beta = reg.slope
        alpha = reg.intercept * 252 * 100
    else:
        beta = np.nan
        alpha = np.nan

    results.append({
        "amfi_code": code,
        "cagr_1yr_pct": calculate_cagr(nav[nav["amfi_code"] == code], 1),
        "cagr_3yr_pct": calculate_cagr(nav[nav["amfi_code"] == code], 3),
        "cagr_5yr_pct": calculate_cagr(nav[nav["amfi_code"] == code], 5),
        "sharpe_ratio": sharpe,
        "sortino_ratio": sortino,
        "alpha_pct": alpha,
        "beta": beta,
        "max_drawdown_pct": max_drawdown,
        "max_drawdown_date": max_drawdown_date
    })

metrics = pd.DataFrame(results)

metrics = metrics.merge(
    funds[["amfi_code", "scheme_name", "fund_house", "category", "sub_category", "expense_ratio_pct"]],
    on="amfi_code",
    how="left"
)

metrics.to_csv(reports / "alpha_beta.csv", index=False)

# Fund scorecard
score = metrics.copy()

score["return_score"] = score["cagr_3yr_pct"].rank(pct=True) * 100
score["sharpe_score"] = score["sharpe_ratio"].rank(pct=True) * 100
score["alpha_score"] = score["alpha_pct"].rank(pct=True) * 100
score["expense_score"] = score["expense_ratio_pct"].rank(ascending=False, pct=True) * 100
score["drawdown_score"] = score["max_drawdown_pct"].rank(pct=True) * 100

score["final_score"] = (
    0.30 * score["return_score"] +
    0.25 * score["sharpe_score"] +
    0.20 * score["alpha_score"] +
    0.15 * score["expense_score"] +
    0.10 * score["drawdown_score"]
)

score = score.sort_values("final_score", ascending=False)

score.to_csv(reports / "fund_scorecard.csv", index=False)

print("Performance analytics completed.")
print("Saved: reports/alpha_beta.csv")
print("Saved: reports/fund_scorecard.csv")
print(score[["scheme_name", "final_score", "cagr_3yr_pct", "sharpe_ratio", "alpha_pct"]].head())

charts_path = reports / "charts"
charts_path.mkdir(exist_ok=True)

top5_codes = score.head(5)["amfi_code"].tolist()

top5_nav = nav[nav["amfi_code"].isin(top5_codes)].copy()
top5_nav = top5_nav[top5_nav["date"] >= top5_nav["date"].max() - pd.DateOffset(years=3)]

pivot_nav = top5_nav.pivot(index="date", columns="amfi_code", values="nav")
normalized_nav = pivot_nav / pivot_nav.iloc[0] * 100

nifty = bench[bench["index_name"].isin(["NIFTY50", "NIFTY100"])].copy()
nifty = nifty[nifty["date"] >= top5_nav["date"].min()]
pivot_bench = nifty.pivot(index="date", columns="index_name", values="close_value")
normalized_bench = pivot_bench / pivot_bench.iloc[0] * 100

plt.figure(figsize=(14, 7))

for code in normalized_nav.columns:
    scheme = funds.loc[funds["amfi_code"] == code, "scheme_name"].values[0][:25]
    plt.plot(normalized_nav.index, normalized_nav[code], label=scheme)

for index_name in normalized_bench.columns:
    plt.plot(normalized_bench.index, normalized_bench[index_name], linestyle="--", label=index_name)

plt.title("Top 5 Funds vs NIFTY 50 and NIFTY 100 - Last 3 Years")
plt.xlabel("Date")
plt.ylabel("Normalized Value (Base = 100)")
plt.legend()
plt.tight_layout()

plt.savefig(charts_path / "benchmark_comparison.png", dpi=300)
plt.close()

print("Saved: reports/charts/benchmark_comparison.png")