import pandas as pd
import json

file = "Tata Steel.xlsx"

df = pd.read_excel(
    file,
    sheet_name="Data Sheet",
    header=None
)

def get_row_value(row_name):
    row = df[df[0] == row_name]

    if row.empty:
        return None

    return row.iloc[0]


def cagr(start, end, years):
    return ((end / start) ** (1 / years) - 1) * 100


# =====================================
# COMPANY INFO
# =====================================

company = df.iloc[0, 1]
current_price = df.iloc[7, 1]
market_cap = df.iloc[8, 1]

# =====================================
# PROFIT & LOSS
# =====================================

sales = get_row_value("Sales")
op_profit = get_row_value("Operating Profit")
net_profit = get_row_value("Net profit")
interest = get_row_value("Interest")

# =====================================
# LATEST VALUES
# =====================================

latest_sales = float(sales.iloc[-1])
latest_op_profit = float(op_profit.iloc[-1])
latest_net_profit = float(net_profit.iloc[-1])
latest_interest = float(interest.iloc[-1])

# =====================================
# LAST 5 YEARS
# =====================================

sales_5y = sales.iloc[-5:]
profit_5y = net_profit.iloc[-5:]

# =====================================
# YOY GROWTH
# =====================================

sales_growth = (
    (sales_5y.iloc[-1] - sales_5y.iloc[-2])
    / sales_5y.iloc[-2]
) * 100

profit_growth = (
    (profit_5y.iloc[-1] - profit_5y.iloc[-2])
    / profit_5y.iloc[-2]
) * 100

# =====================================
# CAGR
# =====================================

if sales_5y.iloc[0] > 0 and sales_5y.iloc[-1] > 0:
    sales_cagr = cagr(
        float(sales_5y.iloc[0]),
        float(sales_5y.iloc[-1]),
        4
    )
else:
    sales_cagr = None

if profit_5y.iloc[0] > 0 and profit_5y.iloc[-1] > 0:
    profit_cagr = cagr(
        float(profit_5y.iloc[0]),
        float(profit_5y.iloc[-1]),
        4
    )
else:
    profit_cagr = None

# =====================================
# MARGINS
# =====================================

opm = (latest_op_profit / latest_sales) * 100

net_margin = (
    latest_net_profit / latest_sales
) * 100

# =====================================
# BALANCE SHEET
# =====================================

equity_capital = get_row_value("Equity Share Capital")
reserves = get_row_value("Reserves")
borrowings = get_row_value("Borrowings")
shares = get_row_value("No. of Equity Shares")

latest_equity_capital = float(equity_capital.iloc[-1])
latest_reserves = float(reserves.iloc[-1])
latest_borrowings = float(borrowings.iloc[-1])
latest_shares = float(shares.iloc[-1])

# Shareholders Equity

shareholders_equity = (
    latest_equity_capital +
    latest_reserves
)

# Debt / Equity

debt_equity = (
    latest_borrowings /
    shareholders_equity
)

# Book Value Per Share

latest_shares_cr = (
    latest_shares / 10000000
)

book_value_per_share = (
    shareholders_equity /
    latest_shares_cr
)
# ROE
# =====================================
# ROCE
# =====================================

capital_employed = (
    shareholders_equity +
    latest_borrowings
)

roce = (
    latest_op_profit /
    capital_employed
) * 100




roe = (
    latest_net_profit /
    shareholders_equity
) * 100

# Interest Coverage

interest_coverage = (
    latest_op_profit /
    latest_interest
)

# Price to Book

price_to_book = (
    float(current_price) /
    book_value_per_share
)

net_block = get_row_value("Net Block")
cash_bank = get_row_value("Cash & Bank")

latest_net_block = float(net_block.iloc[-1])
latest_cash = float(cash_bank.iloc[-1])


# =====================================
# ANALYST INSIGHTS
# =====================================

insights = []

if profit_growth > sales_growth * 2:
    insights.append(
        "Profit growth is significantly higher than revenue growth. Investigate margin expansion, lower costs, or recovery from a weak base."
    )

if net_margin > 5:
    insights.append(
        "Net profit margin appears healthy."
    )
else:
    insights.append(
        "Net profit margin remains relatively weak."
    )

if latest_interest > latest_op_profit * 0.3:
    insights.append(
        "Interest burden appears significant and should be monitored."
    )
else:
    insights.append(
        "Interest burden appears manageable."
    )

if debt_equity > 1:
    insights.append(
        "Leverage is elevated. Debt exceeds shareholders' equity."
    )
elif debt_equity > 0.5:
    insights.append(
        "Moderate leverage profile."
    )
else:
    insights.append(
        "Conservative balance sheet with manageable leverage."
    )

if roe > 15:
    insights.append(
        "ROE indicates strong shareholder value creation."
    )
else:
    insights.append(
        "ROE remains below the preferred threshold of 15%."
    )
if roce > 15:
    insights.append(
        "ROCE indicates efficient deployment of capital."
    )
elif roce > 10:
    insights.append(
        "ROCE is acceptable but leaves room for improvement."
    )
else:
    insights.append(
        "ROCE is relatively low for a capital-intensive business."
    )

if interest_coverage < 2:
    insights.append(
        "Interest coverage is weak, indicating debt servicing pressure."
    )
elif interest_coverage < 4:
    insights.append(
        "Interest coverage is adequate but should be monitored."
    )
else:
    insights.append(
        "Interest coverage is comfortable."
    )
# =====================================
# FINANCIAL HEALTH SCORE
# =====================================

score = 50

if sales_growth > 5:
    score += 10

if profit_growth > 10:
    score += 15

if net_margin > 5:
    score += 10

if latest_interest < latest_op_profit * 0.3:
    score += 15

score = min(score, 100)




# =====================================
# REPORT
# =====================================

report = {
    "company": company,
    "current_price": round(float(current_price), 2),
    "market_cap_cr": round(float(market_cap), 2),
    "latest_sales_cr": round(latest_sales, 2),
    "latest_operating_profit_cr": round(latest_op_profit, 2),
    "latest_net_profit_cr": round(latest_net_profit, 2),
    "sales_growth_pct": round(sales_growth, 2),
    "profit_growth_pct": round(profit_growth, 2),
    "interest_coverage": round(interest_coverage, 2),
    "price_to_book": round(price_to_book, 2),
    "sales_cagr_pct": (
        round(sales_cagr, 2)
        if sales_cagr is not None
        else "Not Meaningful"
    ),
    "interest_coverage": round(interest_coverage, 2),
    "price_to_book": round(price_to_book, 2),
    "roce_pct": round(roce, 2),
    "profit_cagr_pct": (
        round(profit_cagr, 2)
        if profit_cagr is not None
        else "Not Meaningful"
    ),
    "operating_margin_pct": round(opm, 2),
    "net_margin_pct": round(net_margin, 2),
    "financial_health_score": score,
    "insights": insights,
    "shareholders_equity_cr": round(shareholders_equity, 2),
    "borrowings_cr": round(latest_borrowings, 2),
    "debt_equity": round(debt_equity, 2),
    "book_value_per_share": round(book_value_per_share, 2),
    "roe_pct": round(roe, 2)
}


def generate_research_note(report):

    note = f"""
COMPANY: {report['company']}

FINANCIAL HEALTH SCORE: {report['financial_health_score']}/100

VALUATION

Price: ₹{report['current_price']}
P/B: {report['price_to_book']}x

PROFITABILITY

ROE: {report['roe_pct']}%
ROCE: {report['roce_pct']}%

LEVERAGE

Debt/Equity: {report['debt_equity']}
Interest Coverage: {report['interest_coverage']}x

KEY INSIGHTS
"""

    for insight in report["insights"]:
        note += f"\n• {insight}"

    return note

def analyze_company():
    return report


if __name__ == "__main__":
    print(json.dumps(report, indent=4))