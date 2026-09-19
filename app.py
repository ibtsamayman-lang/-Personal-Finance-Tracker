

"""
MoneyFlow - Premium Personal Finance Tracker
Run with:
    python -m streamlit run app.py
"""

from datetime import date
import streamlit as st
import plotly.express as px

from database import Database
from finance_manager import FinanceManager
from models import TransactionType, Category, CATEGORY_ICONS

st.set_page_config(
    page_title="MoneyFlow",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# PREMIUM UI
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --bg: #080B10;
    --surface: #10151D;
    --surface2: #151B24;
    --border: #242C38;
    --text: #F4F7FA;
    --muted: #8D98A8;
    --accent: #69F0C1;
    --accent2: #9B8CFF;
    --danger: #FF6B81;
    --warning: #FFC857;
}

.stApp {
    background:
        radial-gradient(circle at 8% 0%, rgba(105,240,193,.08), transparent 27%),
        radial-gradient(circle at 95% 12%, rgba(155,140,255,.09), transparent 28%),
        var(--bg);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    max-width: 1420px;
    padding: 2.5rem 3.5rem 4rem;
}

h1, h2, h3, h4 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text) !important;
    letter-spacing: -.03em;
}

p, span, label, div {
    color: var(--text);
}

[data-testid="stHeader"] {
    background: transparent;
}

/* Hide Streamlit branding */
#MainMenu, footer {
    visibility: hidden;
}

/* Header */
.hero {
    position: relative;
    padding: 18px 0 28px;
}

.brand-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 38px;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 20px;
    letter-spacing: -.02em;
}

.brand-mark {
    width: 38px;
    height: 38px;
    display: grid;
    place-items: center;
    border-radius: 12px;
    background: linear-gradient(135deg, var(--accent), #B7FFE5);
    color: #07110D;
    box-shadow: 0 0 30px rgba(105,240,193,.18);
}

.status-pill {
    border: 1px solid var(--border);
    background: rgba(16,21,29,.75);
    border-radius: 999px;
    padding: 8px 13px;
    color: var(--muted);
    font-size: 12px;
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(38px, 5vw, 68px);
    line-height: .98;
    font-weight: 600;
    letter-spacing: -.055em;
    margin: 0;
}

.hero-sub {
    color: var(--muted);
    font-size: 15px;
    margin-top: 13px;
}

/* Cards */
.card {
    background: linear-gradient(145deg, rgba(20,26,35,.96), rgba(13,18,25,.96));
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 25px;
    box-shadow: 0 18px 60px rgba(0,0,0,.16);
}

.balance-card {
    min-height: 230px;
    position: relative;
    overflow: hidden;
    background:
        radial-gradient(circle at 92% 10%, rgba(105,240,193,.16), transparent 28%),
        linear-gradient(145deg, #111A1D, #0D1319);
}

.balance-card:after {
    content: "✦";
    position: absolute;
    right: 30px;
    bottom: -30px;
    font-size: 170px;
    color: rgba(105,240,193,.035);
}

.eyebrow {
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: .13em;
    font-size: 11px;
    font-weight: 700;
}

.big-number {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(38px, 4vw, 58px);
    font-weight: 600;
    letter-spacing: -.05em;
    margin: 12px 0 6px;
}

.mini {
    color: var(--muted);
    font-size: 13px;
}

.stat-card {
    min-height: 110px;
}

.stat-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 29px;
    font-weight: 600;
    margin-top: 10px;
    letter-spacing: -.04em;
}

.stat-green { color: var(--accent) !important; }
.stat-purple { color: var(--accent2) !important; }
.stat-red { color: var(--danger) !important; }

.insight-card {
    min-height: 175px;
    position: relative;
    overflow: hidden;
}

.insight-card:after {
    content: "✦";
    position: absolute;
    right: 18px;
    bottom: -28px;
    font-size: 105px;
    color: rgba(105,240,193,.025);
}

.insight-icon {
    font-size: 25px;
    margin-top: 13px;
}

.smart-note {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-top: 14px;
    padding: 15px 18px;
    border: 1px solid rgba(105,240,193,.16);
    border-radius: 16px;
    background: rgba(105,240,193,.045);
    color: #C8D2DD;
    font-size: 13px;
}

.smart-note-icon {
    color: var(--accent);
    font-size: 16px;
}

.section-title {
    margin: 34px 0 14px;
    display: flex;
    justify-content: space-between;
    align-items: end;
}

.section-title h3 {
    margin: 0;
    font-size: 22px;
}

.section-title span {
    color: var(--muted);
    font-size: 12px;
}

/* Last transaction */
.last-transaction {
    display: flex;
    align-items: center;
    gap: 13px;
    padding: 12px 16px;
    margin: 4px 0 20px;
    background: rgba(16,21,29,.72);
    border: 1px solid var(--border);
    border-radius: 15px;
}

.last-dot {
    color: var(--accent);
    font-size: 11px;
    text-shadow: 0 0 12px rgba(105,240,193,.7);
}

.last-time {
    margin-top: 3px;
    color: #C6CED9;
    font-size: 12px;
}

.last-arrow {
    margin-left: auto;
    color: var(--muted);
}

/* Navigation tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(16,21,29,.72);
    border: 1px solid var(--border);
    padding: 7px;
    border-radius: 17px;
    margin: 12px 0 28px;
}

.stTabs [data-baseweb="tab"] {
    height: 40px;
    border-radius: 11px;
    padding: 0 18px;
    color: var(--muted);
    border: none;
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    background: var(--accent) !important;
    color: #07110D !important;
}

/* ============================================================
   INPUTS / SELECTBOX FIX
   Streamlit uses BaseWeb internally, so force the actual
   input/select text colors instead of styling only the wrapper.
   ============================================================ */

div[data-baseweb="input"],
div[data-baseweb="select"] > div,
div[data-testid="stNumberInput"] > div,
div[data-testid="stDateInput"] > div {
    background: #111720 !important;
    border: 1px solid #293240 !important;
    border-radius: 13px !important;
}

/* Number / text / date inputs */
input,
textarea {
    background-color: #111720 !important;
    color: #F4F7FA !important;
    -webkit-text-fill-color: #F4F7FA !important;
    caret-color: #69F0C1 !important;
}

input::placeholder,
textarea::placeholder {
    color: #697586 !important;
    -webkit-text-fill-color: #697586 !important;
}

/* Number input specifically */
div[data-testid="stNumberInput"] input {
    color: #F4F7FA !important;
    -webkit-text-fill-color: #F4F7FA !important;
    background-color: #111720 !important;
    opacity: 1 !important;
}

/* Date input */
div[data-testid="stDateInput"] input {
    color: #F4F7FA !important;
    -webkit-text-fill-color: #F4F7FA !important;
    background-color: #111720 !important;
}

/* Selectbox selected value */
div[data-baseweb="select"] > div {
    background: #111720 !important;
    color: #F4F7FA !important;
}

div[data-baseweb="select"] span,
div[data-baseweb="select"] div,
div[data-baseweb="select"] input {
    color: #F4F7FA !important;
    -webkit-text-fill-color: #F4F7FA !important;
}

/* Dropdown popup */
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
div[data-baseweb="menu"],
ul[role="listbox"],
div[role="listbox"] {
    background: #111720 !important;
    border: 1px solid #293240 !important;
}

/* Every dropdown option */
li[role="option"],
div[role="option"] {
    background: #111720 !important;
    color: #F4F7FA !important;
    -webkit-text-fill-color: #F4F7FA !important;
}

/* Hovered option */
li[role="option"]:hover,
div[role="option"]:hover {
    background: #202936 !important;
    color: #69F0C1 !important;
    -webkit-text-fill-color: #69F0C1 !important;
}

/* Selected option */
li[role="option"][aria-selected="true"],
div[role="option"][aria-selected="true"] {
    background: #18251F !important;
    color: #69F0C1 !important;
    -webkit-text-fill-color: #69F0C1 !important;
}

/* Selectbox arrow */
div[data-baseweb="select"] svg {
    fill: #8D98A8 !important;
}

/* Number input +/- buttons */
div[data-testid="stNumberInput"] button {
    color: #F4F7FA !important;
    background: #151C26 !important;
    border-color: #293240 !important;
}

div[data-testid="stNumberInput"] button:hover {
    color: #69F0C1 !important;
    background: #202936 !important;
}

/* ============================================================
   DATE PICKER / CALENDAR FIX
   Force calendar popup, month/year controls and day numbers
   to stay visible on the dark theme.
   ============================================================ */

/* Calendar popup container */
div[data-baseweb="calendar"],
div[data-baseweb="calendar"] *,
div[data-baseweb="popover"],
div[data-baseweb="popover"] * {
    box-sizing: border-box;
}

/* Calendar background */
div[data-baseweb="calendar"] {
    background: #111720 !important;
    color: #F4F7FA !important;
    border: 1px solid #293240 !important;
    border-radius: 16px !important;
}

/* Calendar header / month / year */
div[data-baseweb="calendar"] header,
div[data-baseweb="calendar"] [role="heading"],
div[data-baseweb="calendar"] button {
    color: #F4F7FA !important;
}

/* Weekday labels */
div[data-baseweb="calendar"] [role="columnheader"],
div[data-baseweb="calendar"] [role="columnheader"] * {
    color: #8D98A8 !important;
    -webkit-text-fill-color: #8D98A8 !important;
}

/* Actual day buttons/numbers */
div[data-baseweb="calendar"] [role="gridcell"],
div[data-baseweb="calendar"] [role="gridcell"] *,
div[data-baseweb="calendar"] [role="button"] {
    color: #F4F7FA !important;
    -webkit-text-fill-color: #F4F7FA !important;
}

/* Calendar day hover */
div[data-baseweb="calendar"] [role="gridcell"]:hover,
div[data-baseweb="calendar"] [role="button"]:hover {
    background: #202936 !important;
    color: #69F0C1 !important;
}

/* Selected day */
div[data-baseweb="calendar"] [aria-selected="true"],
div[data-baseweb="calendar"] [aria-selected="true"] * {
    background: #69F0C1 !important;
    color: #07110D !important;
    -webkit-text-fill-color: #07110D !important;
    border-radius: 9px !important;
}

/* Previous/next month days */
div[data-baseweb="calendar"] [data-outside-current-month="true"],
div[data-baseweb="calendar"] [data-outside-current-month="true"] * {
    color: #596575 !important;
    -webkit-text-fill-color: #596575 !important;
}

/* Calendar navigation arrows */
div[data-baseweb="calendar"] button svg {
    fill: #F4F7FA !important;
    color: #F4F7FA !important;
}

/* Date picker popover */
div[data-baseweb="popover"] {
    background: #111720 !important;
    color: #F4F7FA !important;
    border: 1px solid #293240 !important;
    border-radius: 16px !important;
}

/* Buttons in date picker popup */
div[data-baseweb="popover"] button {
    color: #F4F7FA !important;
}

div[data-baseweb="popover"] button:hover {
    background: #202936 !important;
    color: #69F0C1 !important;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button {
    border: 1px solid var(--border);
    border-radius: 13px;
    min-height: 43px;
    font-weight: 700;
    background: #151C26;
    color: var(--text);
    transition: .2s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    border-color: var(--accent);
    transform: translateY(-1px);
}

.stFormSubmitButton > button[kind="primary"] {
    background: var(--accent);
    color: #07110D;
    border-color: var(--accent);
}

/* Forms */
div[data-testid="stForm"] {
    background: linear-gradient(145deg, #111720, #0E141B);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 28px;
}

/* Metrics */
div[data-testid="stMetric"] {
    background: transparent;
    border: none;
    padding: 0;
}
div[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
}
div[data-testid="stMetricValue"] {
    color: var(--text) !important;
}

/* Progress */
div[data-testid="stProgress"] > div > div {
    background: var(--accent) !important;
}

/* Alerts */
div[data-testid="stAlert"] {
    border-radius: 15px;
    border: 1px solid var(--border);
}

/* Divider */
hr {
    border-color: var(--border) !important;
    margin: 30px 0;
}

/* Activity row */
.activity {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 15px 0;
    border-bottom: 1px solid rgba(36,44,56,.7);
}

.activity-icon {
    width: 44px;
    height: 44px;
    display: grid;
    place-items: center;
    border-radius: 14px;
    background: #171F29;
    font-size: 20px;
}

.activity-main {
    flex: 1;
}

.activity-cat {
    font-weight: 700;
    font-size: 14px;
}

.activity-note {
    color: var(--muted);
    font-size: 12px;
    margin-top: 3px;
}

.activity-amount {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
}

/* Month comparison */
.comparison-row {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 16px;
    margin-bottom: 9px;
    background: #111720;
    border: 1px solid var(--border);
    border-radius: 16px;
}

.comparison-icon {
    width: 34px;
    height: 34px;
    display: grid;
    place-items: center;
    border-radius: 10px;
    background: #18202A;
    font-weight: 700;
}

.comparison-main {
    flex: 1;
}

.comparison-main b {
    display: block;
    font-size: 13px;
}

.comparison-main span {
    display: block;
    color: var(--muted);
    font-size: 11px;
    margin-top: 3px;
}

.comparison-change {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 14px;
}

/* Budget */
.budget-card {
    background: #111720;
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 13px;
}

.budget-top {
    display: flex;
    justify-content: space-between;
    margin-bottom: 12px;
}

.budget-percent {
    color: var(--muted);
    font-size: 12px;
}

/* Saving goals */
.goal-card {
    background: linear-gradient(145deg, #111A1D, #0E141B);
    border: 1px solid rgba(105,240,193,.16);
    border-radius: 22px;
    padding: 21px;
    margin-bottom: 13px;
}
.goal-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}
.goal-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 18px;
    font-weight: 600;
}
.goal-percent {
    color: var(--accent);
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
}
.goal-progress {
    height: 9px;
    background: #252D38;
    border-radius: 99px;
    overflow: hidden;
    margin: 15px 0 10px;
}
.goal-progress > div {
    height: 100%;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    border-radius: 99px;
}
.goal-meta {
    display: flex;
    justify-content: space-between;
    color: var(--muted);
    font-size: 12px;
}

/* Empty state */
.empty {
    text-align: center;
    padding: 55px 20px;
    border: 1px dashed #303A48;
    border-radius: 22px;
    background: rgba(16,21,29,.5);
}

.empty-icon {
    font-size: 40px;
    margin-bottom: 12px;
}

/* Mobile */
@media (max-width: 900px) {
    .block-container {
        padding: 1.2rem 1rem 3rem;
    }
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# STATE
# ============================================================
if "db" not in st.session_state:
    st.session_state.db = Database()

manager = FinanceManager(st.session_state.db)

# Saving Goals are kept in session state so this feature works
# without changing the existing database schema.
if "saving_goals" not in st.session_state:
    st.session_state.saving_goals = []

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="hero">
    <div class="brand-row">
        <div class="brand">
            <div class="brand-mark">✦</div>
            MONEYFLOW
        </div>
        <div class="status-pill">● Personal finance, simplified</div>
    </div>
    <div class="hero-title">Your money.<br><span style="color:#69F0C1;">Your control.</span></div>
    <div class="hero-sub">A smarter view of your income, spending and financial goals.</div>
</div>
""", unsafe_allow_html=True)

# Keep the original "last transaction" feature.
last_info = manager.last_transaction_info()
if last_info is not None:
    st.markdown(f"""
    <div class="last-transaction">
        <div class="last-dot">●</div>
        <div>
            <div class="eyebrow">Last transaction recorded</div>
            <div class="last-time">{last_info['created_at']}</div>
        </div>
        <div class="last-arrow">↗</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="last-transaction">
        <div class="last-dot">●</div>
        <div>
            <div class="eyebrow">Activity status</div>
            <div class="last-time">No transactions yet — start from Add Money.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# NAVIGATION
# ============================================================
tab_dashboard, tab_add, tab_transactions, tab_budgets = st.tabs(
    ["◉  Overview", "＋  Add Money", "↗  Activity", "◎  Budgets"]
)

# ============================================================
# DASHBOARD
# ============================================================
with tab_dashboard:
    balance = manager.get_balance()
    income = manager.get_total_income()
    expenses = manager.get_total_expenses()
    savings_rate = manager.get_savings_rate()

    c1, c2 = st.columns([1.55, 1])

    with c1:
        st.markdown(f"""
        <div class="card balance-card">
            <div class="eyebrow">Current balance</div>
            <div class="big-number">{balance:,.2f}</div>
            <div class="mini">{"You’re currently in deficit — your recorded expenses are higher than your recorded income." if balance < 0 else "Available after recorded income & expenses"}</div>
            <br>
            <div class="mini">{f"⚠ You need {abs(balance):,.2f} to cover the current gap. If this money came from borrowing, credit, or another source, record it so your balance reflects where it came from." if balance < 0 else "✦ Keep an eye on your cash flow — small changes add up."}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="card stat-card">
            <div class="eyebrow">Savings rate</div>
            <div class="stat-value stat-green">{savings_rate:.1f}%</div>
            <div class="mini">of your recorded income</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        x, y = st.columns(2)
        with x:
            st.markdown(f"""
            <div class="card stat-card">
                <div class="eyebrow">Income</div>
                <div class="stat-value stat-purple">{income:,.0f}</div>
                <div class="mini">total</div>
            </div>
            """, unsafe_allow_html=True)
        with y:
            st.markdown(f"""
            <div class="card stat-card">
                <div class="eyebrow">Expenses</div>
                <div class="stat-value stat-red">{expenses:,.0f}</div>
                <div class="mini">total</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-title">
        <h3>Financial pulse</h3>
        <span>Live from your transactions</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**Spending by category**")
        st.caption("This month")
        by_cat = manager.get_current_month_expenses_by_category()

        if by_cat:
            fig = px.pie(
                names=list(by_cat.keys()),
                values=list(by_cat.values()),
                hole=0.68,
            )
            fig.update_traces(
                textposition="inside",
                textinfo="percent",
                hovertemplate="%{label}<br>%{value:,.2f}<extra></extra>",
            )
            fig.update_layout(
                margin=dict(t=10, b=10, l=10, r=10),
                showlegend=True,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#F4F7FA"),
                legend=dict(font=dict(color="#AAB4C2")),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown("""
            <div class="empty">
                <div class="empty-icon">◌</div>
                <b>No spending data yet</b><br>
                <span style="color:#8D98A8">Add an expense to see your spending map.</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**Cash flow**")
        st.caption("Monthly net trend")
        trend = manager.monthly_trend()

        if not trend.empty:
            # Keep the original monthly_trend() data, but make the visual
            # clearly show positive cash flow above zero and negative below it.
            chart_df = trend.copy()

            fig = px.bar(
                chart_df,
                x="month",
                y="signed",
                labels={"signed": "Net Cash Flow", "month": "Month"},
            )

            fig.update_traces(
                marker_line_width=0,
                hovertemplate="<b>%{x}</b><br>Net cash flow: %{y:,.2f}<extra></extra>",
            )

            fig.add_hline(
                y=0,
                line_width=1,
                line_color="#596575",
                opacity=.8,
            )

            fig.update_layout(
                margin=dict(t=20, b=10, l=10, r=10),
                height=330,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#F4F7FA"),
                showlegend=False,
                xaxis=dict(
                    type="category",
                    showgrid=False,
                    color="#8D98A8",
                    title=None,
                ),
                yaxis=dict(
                    gridcolor="#252D38",
                    color="#8D98A8",
                    title=None,
                    zeroline=False,
                ),
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False},
            )
        else:
            st.markdown("""
            <div class="empty">
                <div class="empty-icon">⌁</div>
                <b>Your chart starts here</b><br>
                <span style="color:#8D98A8">Add transactions to build your cash-flow story.</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-title">
        <h3>Budget radar</h3>
        <span>Spending limits</span>
    </div>
    """, unsafe_allow_html=True)

    budget_status = manager.get_budget_status()

    if not budget_status:
        st.markdown("""
        <div class="empty">
            <div class="empty-icon">◎</div>
            <b>No budgets set</b><br>
            <span style="color:#8D98A8">Create category limits from the Budgets tab.</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        for b in budget_status:
            icon = CATEGORY_ICONS.get(Category(b["category"]), "📦")
            percent = min(float(b["percent"]), 100)
            if b["exceeded"]:
                state = "Over budget"
                state_color = "#FF6B81"
            elif b["percent"] >= 80:
                state = "Almost there"
                state_color = "#FFC857"
            else:
                state = "On track"
                state_color = "#69F0C1"

            st.markdown(f"""
            <div class="budget-card">
                <div class="budget-top">
                    <div><b>{icon} {b["category"]}</b></div>
                    <div class="budget-percent" style="color:{state_color}">{state} · {b["percent"]:.0f}%</div>
                </div>
                <div style="height:7px;background:#252D38;border-radius:99px;overflow:hidden;">
                    <div style="width:{percent}%;height:100%;background:{state_color};border-radius:99px;"></div>
                </div>
                <div class="mini" style="margin-top:10px">{b["spent"]:,.2f} / {b["limit"]:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-title">
        <h3>This month vs last month</h3>
        <span>Category movement</span>
    </div>
    """, unsafe_allow_html=True)

    comparison = manager.get_month_comparison()

    if not comparison:
        st.markdown("""
        <div class="empty">
            <div class="empty-icon">⌁</div>
            <b>Not enough data yet</b><br>
            <span style="color:#8D98A8">Keep recording transactions to compare months.</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        for c in comparison:
            if c["change_percent"] > 0:
                arrow = "↗"
                arrow_color = "#FF6B81"
            elif c["change_percent"] < 0:
                arrow = "↘"
                arrow_color = "#69F0C1"
            else:
                arrow = "→"
                arrow_color = "#8D98A8"

            st.markdown(f"""
            <div class="comparison-row">
                <div class="comparison-icon" style="color:{arrow_color}">{arrow}</div>
                <div class="comparison-main">
                    <b>{c['category']}</b>
                    <span>{c['current']:,.2f} this month · {c['previous']:,.2f} last month</span>
                </div>
                <div class="comparison-change" style="color:{arrow_color}">
                    {c['change_percent']:+.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# SAVING GOALS
# ============================================================
st.markdown("""
<div class="section-title">
    <h3>Saving goals</h3>
    <span>Build something you want</span>
</div>
""", unsafe_allow_html=True)

if not st.session_state.saving_goals:
    st.markdown("""
    <div class="empty">
        <div class="empty-icon">🎯</div>
        <b>No saving goals yet</b><br>
        <span style="color:#8D98A8">Create a goal from the Budgets tab and track your progress here.</span>
    </div>
    """, unsafe_allow_html=True)
else:
    goal_cols = st.columns(min(3, len(st.session_state.saving_goals)))
    for i, goal in enumerate(st.session_state.saving_goals):
        target = float(goal["target"])
        saved = float(goal["saved"])
        percent = min(saved / target * 100, 100) if target > 0 else 0
        remaining = max(target - saved, 0)
        with goal_cols[i % len(goal_cols)]:
            st.markdown(f"""
            <div class="goal-card">
                <div class="goal-top">
                    <div class="goal-name">🎯 {goal["name"]}</div>
                    <div class="goal-percent">{percent:.0f}%</div>
                </div>
                <div class="goal-progress">
                    <div style="width:{percent}%;"></div>
                </div>
                <div class="goal-meta">
                    <span>{saved:,.2f} saved</span>
                    <span>{remaining:,.2f} left</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# SMART INSIGHTS
# ============================================================
st.markdown("""
<div class="section-title">
    <h3>Smart insights</h3>
    <span>What your numbers are telling you</span>
</div>
""", unsafe_allow_html=True)

# Build insights from the same data already used by the dashboard.
# No new database tables or dependencies are required.
insight_cat = manager.get_current_month_expenses_by_category()
current_expense_total = sum(float(v) for v in insight_cat.values()) if insight_cat else 0.0

if not insight_cat and not comparison and not budget_status:
    st.markdown("""
    <div class="empty">
        <div class="empty-icon">✦</div>
        <b>Your first insight is waiting</b><br>
        <span style="color:#8D98A8">Add a few transactions and MoneyFlow will start finding patterns for you.</span>
    </div>
    """, unsafe_allow_html=True)
else:
    top_category = max(insight_cat, key=insight_cat.get) if insight_cat else None
    top_amount = float(insight_cat[top_category]) if top_category else 0.0
    top_share = (top_amount / current_expense_total * 100) if current_expense_total else 0.0

    # Find the budget that is closest to / over its limit.
    risky_budget = None
    if budget_status:
        risky_budget = max(budget_status, key=lambda b: float(b["percent"]))

    insight_cols = st.columns(3)

    with insight_cols[0]:
        if top_category:
            st.markdown(f"""
            <div class="card insight-card">
                <div class="eyebrow">Biggest spending area</div>
                <div class="insight-icon">{CATEGORY_ICONS.get(Category(top_category), "📦")}</div>
                <div class="stat-value">{top_category}</div>
                <div class="mini">{top_amount:,.2f} this month · {top_share:.0f}% of your expenses</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card insight-card">
                <div class="eyebrow">Spending snapshot</div>
                <div class="stat-value">No expenses yet</div>
                <div class="mini">Add an expense to discover your main spending area.</div>
            </div>
            """, unsafe_allow_html=True)

    with insight_cols[1]:
        if risky_budget:
            pct = float(risky_budget["percent"])
            remaining = max(float(risky_budget["limit"]) - float(risky_budget["spent"]), 0.0)
            if risky_budget["exceeded"]:
                title = "Budget needs attention"
                detail = f"{risky_budget['category']} is over its limit."
            else:
                title = "Budget to watch"
                detail = f"{risky_budget['category']} has {remaining:,.2f} left."
            st.markdown(f"""
            <div class="card insight-card">
                <div class="eyebrow">Budget radar</div>
                <div class="stat-value">{pct:.0f}% used</div>
                <div class="mini">{detail}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card insight-card">
                <div class="eyebrow">Budget radar</div>
                <div class="stat-value">No limits yet</div>
                <div class="mini">Set a budget to get early spending alerts.</div>
            </div>
            """, unsafe_allow_html=True)

    with insight_cols[2]:
        if savings_rate > 0:
            if savings_rate >= 20:
                message = "You are keeping a solid share of recorded income."
            else:
                message = "There is room to increase the amount you keep."
            rate_text = f"{savings_rate:.1f}%"
        elif income > 0:
            message = "Your recorded expenses currently match or exceed income."
            rate_text = "0%"
        else:
            message = "Add income to see your savings picture."
            rate_text = "—"

        st.markdown(f"""
        <div class="card insight-card">
            <div class="eyebrow">Savings signal</div>
            <div class="stat-value stat-green">{rate_text}</div>
            <div class="mini">{message}</div>
        </div>
        """, unsafe_allow_html=True)

    if top_category and current_expense_total > 0:
        st.markdown(f"""
        <div class="smart-note">
            <span class="smart-note-icon">✦</span>
            <div><b>MoneyFlow noticed:</b> {top_category} is your largest spending category this month, accounting for {top_share:.0f}% of recorded expenses.</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# ADD TRANSACTION
# ============================================================
with tab_add:
    st.markdown("""
    <div class="section-title">
        <h3>Record a transaction</h3>
        <span>Keep your financial picture up to date</span>
    </div>
    """, unsafe_allow_html=True)

    with st.form("add_transaction_form", clear_on_submit=True):
        st.markdown("### What happened?")

        c1, c2 = st.columns(2)
        t_type = c1.selectbox("Transaction type", [t.value for t in TransactionType])
        t_category = c2.selectbox("Category", [c.value for c in Category])

        c3, c4 = st.columns(2)
        t_amount = c3.number_input("Amount", min_value=0.0, step=0.01, format="%.2f", value=0.0)
        t_date = c4.date_input("Date", value=date.today())

        t_note = st.text_input(
            "Note",
            placeholder="e.g. Groceries, monthly salary, transport..."
        )

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("＋  Add Transaction", type="primary", use_container_width=True)

        if submitted:
            if t_amount <= 0:
                st.error("Amount must be greater than zero.")
            else:
                manager.add_transaction(
                    t_type,
                    t_category,
                    t_amount,
                    t_note,
                    t_date.strftime("%Y-%m-%d"),
                )
                st.success(f"Added {t_type.lower()} of {t_amount:,.2f} in {t_category}.")
                st.rerun()

# ============================================================
# TRANSACTIONS
# ============================================================
with tab_transactions:
    transactions = manager.get_all()

    st.markdown("""
    <div class="section-title">
        <h3>Activity</h3>
        <span>Your financial timeline</span>
    </div>
    """, unsafe_allow_html=True)

    if not transactions:
        st.markdown("""
        <div class="empty">
            <div class="empty-icon">✦</div>
            <b>No transactions yet</b><br>
            <span style="color:#8D98A8">Your activity will appear here once you add your first transaction.</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        filter_type = st.selectbox(
            "Filter",
            ["All"] + [t.value for t in TransactionType],
        )

        filtered = (
            transactions
            if filter_type == "All"
            else [t for t in transactions if t.type == filter_type]
        )

        for t in filtered:
            sign = "+" if t.type == TransactionType.INCOME.value else "-"
            amount_color = "#69F0C1" if sign == "+" else "#FF6B81"

            c1, c2, c3 = st.columns([5, 2, .8])

            with c1:
                st.markdown(f"""
                <div class="activity">
                    <div class="activity-icon">{t.icon()}</div>
                    <div class="activity-main">
                        <div class="activity-cat">{t.category}</div>
                        <div class="activity-note">{t.note or "No note"} · {t.date}</div>
                    </div>
                    <div class="activity-amount" style="color:{amount_color}">
                        {sign}{t.amount:,.2f}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with c3:
                if st.button("×", key=f"del_{t.id}", help="Delete transaction"):
                    manager.delete_transaction(t.id)
                    st.rerun()

# ============================================================
# BUDGETS
# ============================================================
with tab_budgets:
    st.markdown("""
    <div class="section-title">
        <h3>Budget studio</h3>
        <span>Give every category a limit</span>
    </div>
    """, unsafe_allow_html=True)

    with st.form("budget_form"):
        b_category = st.selectbox(
            "Category",
            [c.value for c in Category if c != Category.SALARY],
        )
        b_limit = st.number_input(
            "Monthly limit",
            min_value=0.0,
            step=0.01,
            format="%.2f",
            value=0.0,
        )

        if st.form_submit_button("◎  Save Budget", type="primary", use_container_width=True):
            if b_limit > 0:
                st.session_state.db.set_budget(b_category, b_limit)
                st.success(f"Budget for {b_category} set to {b_limit:,.2f}.")
                st.rerun()
            else:
                st.error("Budget must be greater than zero.")

    st.markdown("""
    <div class="section-title">
        <h3>Saving goals</h3>
        <span>Turn plans into progress</span>
    </div>
    """, unsafe_allow_html=True)

    with st.form("saving_goal_form"):
        g_name = st.text_input(
            "Goal name",
            placeholder="e.g. New laptop, Emergency fund, Trip..."
        )
        g_target = st.number_input(
            "Target amount",
            min_value=0.0,
            step=0.01,
            format="%.2f",
            value=0.0,
        )
        g_saved = st.number_input(
            "Already saved",
            min_value=0.0,
            step=0.01,
            format="%.2f",
            value=0.0,
        )

        if st.form_submit_button("🎯  Create Saving Goal", type="primary", use_container_width=True):
            if not g_name.strip():
                st.error("Enter a name for your goal.")
            elif g_target <= 0:
                st.error("Target amount must be greater than zero.")
            elif g_saved < 0 or g_saved > g_target:
                st.error("Saved amount must be between 0 and the target amount.")
            else:
                st.session_state.saving_goals.append({
                    "name": g_name.strip(),
                    "target": float(g_target),
                    "saved": float(g_saved),
                })
                st.success(f"Saving goal '{g_name.strip()}' created.")
                st.rerun()

    if st.session_state.saving_goals:
        for i, goal in enumerate(st.session_state.saving_goals):
            target = float(goal["target"])
            saved = float(goal["saved"])
            percent = min(saved / target * 100, 100) if target > 0 else 0
            remaining = max(target - saved, 0)

            st.markdown(f"""
            <div class="goal-card">
                <div class="goal-top">
                    <div class="goal-name">🎯 {goal["name"]}</div>
                    <div class="goal-percent">{percent:.0f}%</div>
                </div>
                <div class="goal-progress">
                    <div style="width:{percent}%;"></div>
                </div>
                <div class="goal-meta">
                    <span>{saved:,.2f} / {target:,.2f}</span>
                    <span>{remaining:,.2f} remaining</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            gc1, gc2 = st.columns(2)
            with gc1:
                new_saved = st.number_input(
                    f"Update saved amount — {goal['name']}",
                    min_value=0.0,
                    max_value=target,
                    value=saved,
                    step=0.01,
                    format="%.2f",
                    key=f"goal_saved_{i}",
                )
            with gc2:
                if st.button("Update progress", key=f"update_goal_{i}", use_container_width=True):
                    st.session_state.saving_goals[i]["saved"] = float(new_saved)
                    st.rerun()

            if st.button("Remove goal", key=f"remove_goal_{i}"):
                st.session_state.saving_goals.pop(i)
                st.rerun()

    st.markdown("""
    <div class="section-title">
        <h3>Current limits</h3>
        <span>Monthly</span>
    </div>
    """, unsafe_allow_html=True)

    budgets = st.session_state.db.get_budgets()

    if not budgets:
        st.markdown("""
        <div class="empty">
            <div class="empty-icon">◎</div>
            <b>Your budget is empty</b><br>
            <span style="color:#8D98A8">Set your first category limit above.</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        for cat, limit in budgets.items():
            icon = CATEGORY_ICONS.get(Category(cat), "📦")
            st.markdown(f"""
            <div class="budget-card">
                <div class="budget-top">
                    <b>{icon} {cat}</b>
                    <b>{limit:,.2f} / month</b>
                </div>
                <div class="mini">Your spending limit for this category.</div>
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# FOOTER / SAFE CLEAR
# ============================================================
st.markdown("<br><hr>", unsafe_allow_html=True)

with st.expander("⚠️ Data management"):
    st.caption("Clearing data permanently removes all recorded transactions and budgets from the local database.")
    if st.button("Clear All Data", type="secondary"):
        st.session_state.db.clear_all()
        st.success("All data cleared.")
        st.rerun()

st.markdown("""
<div style="text-align:center;color:#596575;font-size:11px;padding-top:12px;">
    MONEYFLOW · Personal Finance Tracker
</div>
""", unsafe_allow_html=True)
