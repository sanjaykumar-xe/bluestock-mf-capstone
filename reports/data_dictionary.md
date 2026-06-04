# Data Dictionary

## 01_fund_master
- amfi_code : Unique scheme identifier
- fund_house : Mutual fund company
- scheme_name : Scheme name
- category : Equity/Debt
- sub_category : Scheme type
- plan : Direct/Regular
- launch_date : Scheme launch date
- benchmark : Benchmark index
- expense_ratio_pct : Expense ratio
- exit_load_pct : Exit load percentage
- min_sip_amount : Minimum SIP amount
- min_lumpsum_amount : Minimum lumpsum amount
- fund_manager : Fund manager
- risk_category : Risk category
- sebi_category_code : SEBI category code

## 02_nav_history
- amfi_code : Scheme code
- date : NAV date
- nav : Net Asset Value

## 07_scheme_performance
- return_1yr_pct : 1-year return
- return_3yr_pct : 3-year return
- return_5yr_pct : 5-year return
- benchmark_3yr_pct : Benchmark return
- alpha : Alpha metric
- beta : Beta metric
- sharpe_ratio : Sharpe ratio
- expense_ratio_pct : Expense ratio
- aum_crore : Assets under management

## 08_investor_transactions
- investor_id : Investor identifier
- transaction_date : Transaction date
- transaction_type : SIP/Lumpsum/Redemption
- amount_inr : Transaction amount
- state : Investor state
- city : Investor city
- kyc_status : KYC verification status