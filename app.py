import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Jordan SSC Calculator", layout="wide")

st.title("Jordan Social Security – Pension Calculator")

# --------------------
# INPUTS
# --------------------
with st.sidebar:
    st.header("Inputs")
    start_age = st.number_input("Start age", 18, 70, 38)
    retire_age = st.number_input("Retirement age", 50, 70, 60)
    existing_months = st.number_input("Existing contribution months", 0, 600, 52)

    last_wage = st.number_input("Last insured wage (JD)", 0.0, 50000.0, 1552.0)
    ceiling = st.number_input("Wage ceiling (JD)", 0.0, 50000.0, 3668.0)

    contrib_rate = st.number_input("Contribution rate", 0.0, 1.0, 0.2175)
    inc_pct = st.number_input("Annual increase %", 0.0, 0.3, 0.10)
    inc_every = st.number_input("Increase every N years", 1, 5, 2)
    inc_start_age = st.number_input("Increase start age", 18, 70, start_age)

# --------------------
# BUILD TABLE
# --------------------
ages = list(range(start_age, retire_age))
wage = last_wage
rows = []
cumulative = 0

for age in ages:
    if age >= inc_start_age and (age - inc_start_age) % inc_every == 0:
        wage = min(wage * (1 + inc_pct), ceiling)

    monthly = wage * contrib_rate
    annual = monthly * 12
    cumulative += annual

    rows.append([
        age,
        round(wage, 0),
        round(monthly, 2),
        round(annual, 2),
        round(cumulative, 2)
    ])

df = pd.DataFrame(rows, columns=[
    "Age", "Wage", "Monthly payment", "Annual payment", "Cumulative paid"
])

st.subheader("Annual contribution table")
st.dataframe(df, use_container_width=True)

# --------------------
# PENSION ESTIMATION
# --------------------
years = (existing_months + len(ages)*12) / 12
avg_wage = df.tail(3)["Wage"].mean()

pension = years * (
    min(avg_wage, 1500) * 0.025 +
    max(avg_wage - 1500, 0) * 0.02
)

st.subheader("Results")
st.metric("Estimated monthly pension (JD)", round(pension, 0))
st.metric("Total paid (JD)", round(cumulative, 0))
st.metric("Years to breakeven", round(cumulative / (pension*12), 1))

st.line_chart(df.set_index("Age")["Cumulative paid"])
