-- 1. Top 5 Funds by AUM
SELECT scheme_name, aum_crore
FROM "07_scheme_performance"
ORDER BY aum_crore DESC
LIMIT 5;

-- 2. Average NAV by Fund
SELECT amfi_code, AVG(nav) AS avg_nav
FROM "02_nav_history"
GROUP BY amfi_code;

-- 3. Total SIP Transactions
SELECT COUNT(*) AS sip_count
FROM "08_investor_transactions"
WHERE transaction_type='Sip';

-- 4. Transactions by State
SELECT state, COUNT(*) AS total_transactions
FROM "08_investor_transactions"
GROUP BY state
ORDER BY total_transactions DESC;

-- 5. Funds with Expense Ratio < 1%
SELECT scheme_name, expense_ratio_pct
FROM "07_scheme_performance"
WHERE expense_ratio_pct < 1;

-- 6. Average Return by Category
SELECT category, AVG(return_3yr_pct)
FROM "07_scheme_performance"
GROUP BY category;

-- 7. Top Fund Houses by AUM
SELECT fund_house, SUM(aum_crore)
FROM "07_scheme_performance"
GROUP BY fund_house
ORDER BY SUM(aum_crore) DESC;

-- 8. Average Transaction Amount
SELECT AVG(amount_inr)
FROM "08_investor_transactions";

-- 9. KYC Status Distribution
SELECT kyc_status, COUNT(*)
FROM "08_investor_transactions"
GROUP BY kyc_status;

-- 10. Portfolio Holdings by Sector
SELECT sector, COUNT(*)
FROM "09_portfolio_holdings"
GROUP BY sector
ORDER BY COUNT(*) DESC;