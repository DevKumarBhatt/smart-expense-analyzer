
import streamlit as st
import pandas as pd
import plotly.express as px

from datetime import date

from database import (
    create_table,
    add_transaction,
    get_transactions,
    create_budget_table,
    save_budget,
    get_budgets,
)

st.set_page_config(
    page_title="Smart Expense Analyzer",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- DATABASE ----------

create_table()
create_budget_table()

# ---------- DARK MODERN UI ----------

st.markdown("""
<style>
    .stApp {
        background:
            radial-gradient(ellipse at 10% 0%, #102b24 0%, transparent 35%),
            radial-gradient(ellipse at 90% 10%, #101d32 0%, transparent 30%),
            #080b10;
        color: #f1f5f9;
    }

    [data-testid="stSidebar"] {
        background: #0b1017;
        border-right: 1px solid #1c2933;
    }

    [data-testid="stHeader"] {
        background: rgba(8, 11, 16, 0.85);
    }

    h1, h2, h3 {
        color: #f8fafc !important;
        letter-spacing: -0.5px;
    }

    p, label, span {
        color: #cbd5e1;
    }

    .hero {
        padding: 25px 28px;
        border: 1px solid #244438;
        border-radius: 18px;
        background: linear-gradient(120deg, #10241e, #101722 70%);
        box-shadow: 0 0 28px rgba(34, 197, 94, 0.08);
        margin-bottom: 24px;
    }

    .hero-tag {
        color: #4ade80;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .hero h1 {
        margin: 8px 0 5px;
        font-size: 34px;
    }

    .hero p {
        margin-bottom: 0;
        color: #a7b5c4;
    }

    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #121a22, #0c1219);
        border: 1px solid #24323d;
        padding: 19px;
        border-radius: 15px;
        box-shadow: 0 0 18px rgba(34, 197, 94, 0.04);
    }

    [data-testid="stMetricLabel"] {
        color: #9caebb !important;
    }

    [data-testid="stMetricValue"] {
        color: #4ade80 !important;
        font-weight: 700;
    }

    [data-testid="stForm"] {
        background: #0d141c;
        border: 1px solid #263540;
        padding: 20px;
        border-radius: 15px;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        background: linear-gradient(90deg, #16a34a, #22c55e);
        color: #04110a;
        font-weight: 700;
        border: none;
        border-radius: 9px;
        min-height: 42px;
        transition: 0.2s ease;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        background: #4ade80;
        color: #04110a;
        box-shadow: 0 0 18px rgba(34, 197, 94, 0.25);
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #24323d;
        border-radius: 12px;
        overflow: hidden;
    }

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        background: #111923;
        border-color: #344452;
    }

    hr {
        border-color: #24323d;
    }

    .section-note {
        color: #8fa2b3;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------

st.markdown("""
<div class="hero">
    <div class="hero-tag">PERSONAL FINANCE DASHBOARD</div>
    <h1>Smart Expense Analyzer</h1>
    <p>Track your money. Control your spending. Build better habits.</p>
</div>
""", unsafe_allow_html=True)

# ---------- LOAD DATA ----------

rows = get_transactions()

df = pd.DataFrame(
    rows,
    columns=["Date", "Type", "Category", "Amount", "Description"],
)

if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Amount"] = pd.to_numeric(
        df["Amount"], errors="coerce"
    ).fillna(0)
    df = df.dropna(subset=["Date"])

# ---------- SIDEBAR ----------

st.sidebar.markdown("## 💸 Money Manager")
st.sidebar.caption("Your personal finance workspace")

page = st.sidebar.radio(
    "NAVIGATION",
    ["Dashboard", "Transactions", "Monthly Budget"],
)

st.sidebar.divider()
st.sidebar.caption("SMART EXPENSE ANALYZER")
st.sidebar.caption("Built with Python + Streamlit")

# ---------- DASHBOARD ----------

if page == "Dashboard":

    st.subheader("📊 Financial Overview")
    st.caption("Your financial snapshot across all recorded transactions.")

    if df.empty:
        income = 0.0
        expenses = 0.0
    else:
        income = df.loc[
            df["Type"] == "Income", "Amount"
        ].sum()

        expenses = df.loc[
            df["Type"] == "Expense", "Amount"
        ].sum()

    balance = income - expenses

    c1, c2, c3 = st.columns(3)
    c1.metric("💰 Total Income", f"₹{income:,.2f}")
    c2.metric("💸 Total Expenses", f"₹{expenses:,.2f}")
    c3.metric("📈 Net Balance", f"₹{balance:,.2f}")

    st.divider()

    st.subheader("➕ Add a Transaction")

    with st.form("transaction_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            transaction_type = st.selectbox(
                "Transaction Type",
                ["Expense", "Income"],
            )

            amount = st.number_input(
                "Amount (₹)",
                min_value=1.0,
                value=100.0,
                step=50.0,
            )

            transaction_date = st.date_input(
                "Transaction Date",
                value=date.today(),
            )

        with col2:
            category = st.selectbox(
                "Category",
                [
                    "Food",
                    "Transport",
                    "Shopping",
                    "Bills",
                    "Education",
                    "Health",
                    "Salary",
                    "Other",
                ],
            )

            description = st.text_input(
                "Description",
                placeholder="e.g. Grocery shopping",
            )

        submitted = st.form_submit_button(
            "Save Transaction",
            use_container_width=True,
        )

    if submitted:
        add_transaction(
            transaction_date,
            transaction_type,
            category,
            amount,
            description,
        )
        st.success("Transaction saved successfully!")
        st.rerun()

    st.divider()

    # Monthly expense chart
    st.subheader("📉 Spending Analytics")

    selected_date = st.date_input(
        "Choose month for analytics",
        value=date.today().replace(day=1),
        key="analytics_month",
    )

    selected_month = selected_date.strftime("%Y-%m")

    if not df.empty:
        month_df = df[
            (df["Date"].dt.strftime("%Y-%m") == selected_month)
            & (df["Type"] == "Expense")
        ]
    else:
        month_df = pd.DataFrame(columns=df.columns)

    if not month_df.empty:
        category_totals = (
            month_df.groupby("Category", as_index=False)["Amount"]
            .sum()
        )

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            fig = px.pie(
                category_totals,
                names="Category",
                values="Amount",
                hole=0.62,
                title="Expense Distribution",
                color_discrete_sequence=[
                    "#4ade80",
                    "#38bdf8",
                    "#a78bfa",
                    "#fbbf24",
                    "#fb7185",
                    "#2dd4bf",
                    "#818cf8",
                ],
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0",
                legend_title_text="Category",
                margin=dict(t=55, b=10, l=10, r=10),
            )
            st.plotly_chart(fig, use_container_width=True)

        with chart_col2:
            bar = px.bar(
                category_totals.sort_values(
                    "Amount", ascending=True
                ),
                x="Amount",
                y="Category",
                orientation="h",
                title="Spending by Category",
                text="Amount",
                color="Amount",
                color_continuous_scale=["#14532d", "#4ade80"],
            )
            bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0",
                coloraxis_showscale=False,
                xaxis_title="Amount (₹)",
                yaxis_title="",
                margin=dict(t=55, b=10, l=10, r=10),
            )
            st.plotly_chart(bar, use_container_width=True)
    else:
        st.info(
            f"No expenses recorded for {selected_month}. "
            "Add an expense to see your charts."
        )

    st.divider()

    st.subheader("🕒 Recent Transactions")

    if not df.empty:
        recent = df.copy()
        recent["Date"] = recent["Date"].dt.strftime("%d %b %Y")
        st.dataframe(
            recent.head(5),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No transactions yet. Add your first transaction above.")

# ---------- TRANSACTIONS PAGE ----------

elif page == "Transactions":

    st.subheader("📋 Transaction History")
    st.caption("Review and export your recorded transactions.")

    if not df.empty:
        search = st.text_input(
            "Search by category or description",
            placeholder="e.g. Food or groceries",
        )

        filtered = df.copy()

        if search.strip():
            mask = (
                filtered["Category"].str.contains(
                    search, case=False, na=False
                )
                | filtered["Description"].fillna("").str.contains(
                    search, case=False, na=False
                )
            )
            filtered = filtered[mask]

        type_filter = st.selectbox(
            "Filter by type",
            ["All", "Income", "Expense"],
        )

        if type_filter != "All":
            filtered = filtered[filtered["Type"] == type_filter]

        display_df = filtered.copy()
        display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "⬇️ Download CSV Report",
            data=display_df.to_csv(index=False).encode("utf-8"),
            file_name="transactions.csv",
            mime="text/csv",
        )

        st.caption(f"Showing {len(display_df)} transaction(s).")
    else:
        st.info("No transactions available yet.")

# ---------- MONTHLY BUDGET PAGE ----------

elif page == "Monthly Budget":

    st.subheader("🎯 Monthly Budget & Alerts")
    st.caption("Set spending limits and monitor your monthly expenses.")

    chosen_date = st.date_input(
        "Select month",
        value=date.today().replace(day=1),
        key="budget_month",
    )
    selected_month = chosen_date.strftime("%Y-%m")

    budget_categories = [
        "Food",
        "Transport",
        "Shopping",
        "Bills",
        "Education",
        "Health",
        "Other",
    ]

    with st.form("budget_form"):
        st.markdown("### Set or update a category budget")

        budget_category = st.selectbox(
            "Budget Category",
            budget_categories,
        )

        budget_amount = st.number_input(
            "Monthly Budget (₹)",
            min_value=1.0,
            value=5000.0,
            step=500.0,
        )

        budget_submitted = st.form_submit_button(
            "Save Budget",
            use_container_width=True,
        )

    if budget_submitted:
        save_budget(
            selected_month,
            budget_category,
            budget_amount,
        )
        st.success(
            f"{budget_category} budget saved for {selected_month}!"
        )
        st.rerun()

    budgets = get_budgets(selected_month)

    if not df.empty:
        monthly_df = df[
            (df["Date"].dt.strftime("%Y-%m") == selected_month)
            & (df["Type"] == "Expense")
        ]
    else:
        monthly_df = pd.DataFrame(columns=df.columns)

    if budgets:
        budget_df = pd.DataFrame(
            budgets,
            columns=["Category", "Budget"],
        )

        if not monthly_df.empty:
            spending_df = (
                monthly_df.groupby("Category", as_index=False)["Amount"]
                .sum()
                .rename(columns={"Amount": "Spent"})
            )
        else:
            spending_df = pd.DataFrame(
                columns=["Category", "Spent"]
            )

        report = budget_df.merge(
            spending_df,
            on="Category",
            how="left",
        )

        report["Spent"] = report["Spent"].fillna(0.0)
        report["Remaining"] = report["Budget"] - report["Spent"]
        report["Used (%)"] = (
            report["Spent"] / report["Budget"] * 100
        ).round(1)

        st.divider()
        st.markdown(f"### Budget Report — {selected_month}")

        st.dataframe(
            report,
            column_config={
                "Budget": st.column_config.NumberColumn(
                    "Budget", format="₹%.2f"
                ),
                "Spent": st.column_config.NumberColumn(
                    "Spent", format="₹%.2f"
                ),
                "Remaining": st.column_config.NumberColumn(
                    "Remaining", format="₹%.2f"
                ),
                "Used (%)": st.column_config.NumberColumn(
                    "Used (%)", format="%.1f%%"
                ),
            },
            use_container_width=True,
            hide_index=True,
        )

        for _, row in report.iterrows():
            st.markdown(f"**{row['Category']}**")

            progress = min(
                max(float(row["Used (%)"]) / 100, 0.0),
                1.0,
            )
            st.progress(progress, text=f"{row['Used (%)']:.1f}% used")

            if row["Spent"] > row["Budget"]:
                st.error(
                    f"Budget exceeded by "
                    f"₹{row['Spent'] - row['Budget']:,.2f}"
                )
            elif row["Used (%)"] >= 80:
                st.warning(
                    f"Budget is {row['Used (%)']:.1f}% used."
                )
            else:
                st.success("Spending is within budget.")
    else:
        st.info(
            "No budget set for this month. Save a category budget above "
            "to start tracking your spending."
        )
