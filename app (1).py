import streamlit as st
import json
import os
from datetime import datetime

# ---------- CONFIG ----------
st.set_page_config(page_title="Budget Tracker", page_icon="💸", layout="wide")
DATA_FILE = "data.json"

ICONS = {
    'Salary': '💼', 'Freelance': '🖥️', 'Business': '🏢', 'Investment': '📈', 'Gift': '🎁',
    'Food': '🍽️', 'Rent': '🏠', 'Transport': '🚗', 'Utilities': '💡', 'Shopping': '🛍️',
    'Healthcare': '🏥', 'Entertainment': '🎬', 'Education': '📚', 'EMI / Loan': '🏦', 'Other': '💰'
}

INCOME_CATEGORIES = ["Salary", "Freelance", "Business", "Investment", "Gift", "Other"]
EXPENSE_CATEGORIES = ["Food", "Rent", "Transport", "Utilities", "Shopping",
                      "Healthcare", "Entertainment", "Education", "EMI / Loan", "Other"]

# ---------- DATA HELPERS ----------
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE) as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

if "transactions" not in st.session_state:
    st.session_state.transactions = load_data()

def add_transaction(t_type, desc, amount, category):
    st.session_state.transactions.insert(0, {
        "id": int(datetime.now().timestamp() * 1000),
        "type": t_type,
        "desc": desc,
        "amount": float(amount),
        "category": category,
        "date": datetime.now().strftime("%d/%m/%Y")
    })
    save_data(st.session_state.transactions)

def delete_transaction(txid):
    st.session_state.transactions = [t for t in st.session_state.transactions if t["id"] != txid]
    save_data(st.session_state.transactions)

def clear_all():
    st.session_state.transactions = []
    save_data([])

# ---------- STYLES ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"]  {
    font-family: 'Space Grotesk', sans-serif;
}

:root{
  --bg:#0f1117; --surface:#181c27; --surface2:#1e2335; --border:#2a2f45;
  --income:#22d3a5; --expense:#f45b7a; --savings:#6c8cf4; --text:#e8eaf2; --muted:#7880a0;
}

.stApp { background-color: var(--bg); color: var(--text); }

.card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 14px; padding: 22px; margin-bottom: 10px;
}

.scard { position: relative; overflow: hidden; }
.scard .lbl {
  font-size: .72rem; text-transform: uppercase; letter-spacing: .1em;
  color: var(--muted); font-family: 'DM Mono', monospace; margin-bottom: 6px;
}
.scard .amt { font-size: 1.9rem; font-weight: 700; letter-spacing: -1px; line-height: 1; }
.scard .sub { font-size: .75rem; color: var(--muted); margin-top: 8px; }
.inc-color { color: var(--income); }
.exp-color { color: var(--expense); }
.sav-color { color: var(--savings); }

.tx {
  background: var(--surface2); border: 1px solid var(--border); border-radius: 10px;
  padding: 12px 16px; display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 8px;
}
.tx-left { display: flex; align-items: center; gap: 12px; }
.tx-icon {
  width: 34px; height: 34px; border-radius: 9px; display: flex;
  align-items: center; justify-content: center; font-size: 1rem; flex-shrink: 0;
}
.tx-icon.inc { background: rgba(34,211,165,.13); }
.tx-icon.exp { background: rgba(244,91,122,.13); }
.tx-name { font-size: .9rem; font-weight: 500; }
.tx-meta { font-size: .7rem; color: var(--muted); font-family: 'DM Mono', monospace; margin-top: 2px; }
.tx-amt { font-family: 'DM Mono', monospace; font-size: .95rem; font-weight: 500; }

.empty {
  text-align: center; color: var(--muted); padding: 30px;
  border: 1px dashed var(--border); border-radius: 14px;
}

div[data-testid="stButton"] button {
    border-radius: 8px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
month_str = datetime.now().strftime("%B %Y").upper()
h1, h2 = st.columns([3, 1])
with h1:
    st.markdown("### 💸 Budget Tracker")
with h2:
    st.markdown(f"<div style='text-align:right;color:var(--muted);font-family:DM Mono, monospace;padding-top:14px;'>{month_str}</div>", unsafe_allow_html=True)

st.divider()

# ---------- SUMMARY ----------
transactions = st.session_state.transactions
income = sum(t["amount"] for t in transactions if t["type"] == "income")
expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
savings = income - expense
rate = round((savings / income * 100)) if income > 0 else 0

c1, c2, c3 = st.columns(3)
with c1:
    n_inc = len([t for t in transactions if t["type"] == "income"])
    st.markdown(f"""
    <div class="card scard">
        <div class="lbl">Total Income</div>
        <div class="amt inc-color">₹{income:,.2f}</div>
        <div class="sub">{n_inc} entries</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    n_exp = len([t for t in transactions if t["type"] == "expense"])
    st.markdown(f"""
    <div class="card scard">
        <div class="lbl">Total Expenses</div>
        <div class="amt exp-color">₹{expense:,.2f}</div>
        <div class="sub">{n_exp} entries</div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    sav_class = "exp-color" if savings < 0 else "sav-color"
    sign = "-" if savings < 0 else ""
    st.markdown(f"""
    <div class="card scard">
        <div class="lbl">Net Savings</div>
        <div class="amt {sav_class}">{sign}₹{abs(savings):,.2f}</div>
        <div class="sub">{rate}% of income</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ---------- FORMS ----------
f1, f2 = st.columns(2)

with f1:
    with st.container(border=True):
        st.markdown("##### 🟢 Add Income")
        with st.form("income_form", clear_on_submit=True):
            desc = st.text_input("Description", placeholder="e.g. Monthly salary")
            amount = st.number_input("Amount (₹)", min_value=0.01, step=100.0, format="%.2f")
            category = st.selectbox("Category", INCOME_CATEGORIES)
            submitted = st.form_submit_button("+ Add Income", use_container_width=True)
            if submitted:
                if desc.strip() == "":
                    st.warning("Please enter a description.")
                else:
                    add_transaction("income", desc, amount, category)
                    st.rerun()

with f2:
    with st.container(border=True):
        st.markdown("##### 🔴 Add Expense")
        with st.form("expense_form", clear_on_submit=True):
            desc = st.text_input("Description", placeholder="e.g. Grocery shopping")
            amount = st.number_input("Amount (₹)", min_value=0.01, step=100.0, format="%.2f", key="exp_amt")
            category = st.selectbox("Category", EXPENSE_CATEGORIES)
            submitted = st.form_submit_button("+ Add Expense", use_container_width=True)
            if submitted:
                if desc.strip() == "":
                    st.warning("Please enter a description.")
                else:
                    add_transaction("expense", desc, amount, category)
                    st.rerun()

st.write("")

# ---------- TRANSACTIONS ----------
with st.container(border=True):
    th1, th2 = st.columns([4, 1])
    with th1:
        st.markdown("##### 📋 Transactions")
    with th2:
        if st.button("Clear All", use_container_width=True):
            clear_all()
            st.rerun()

    if not transactions:
        st.markdown("""
        <div class="empty">
            <div style="font-size:2rem;margin-bottom:8px;">💸</div>
            No transactions yet. Add income or expense above.
        </div>
        """, unsafe_allow_html=True)
    else:
        for t in transactions:
            icon = ICONS.get(t["category"], "💰")
            type_class = "inc" if t["type"] == "income" else "exp"
            sign = "+" if t["type"] == "income" else "-"
            color = "inc-color" if t["type"] == "income" else "exp-color"

            row_left, row_right = st.columns([6, 1])
            with row_left:
                st.markdown(f"""
                <div class="tx">
                    <div class="tx-left">
                        <div class="tx-icon {type_class}">{icon}</div>
                        <div>
                            <div class="tx-name">{t['desc']}</div>
                            <div class="tx-meta">{t['category']} · {t['date']}</div>
                        </div>
                    </div>
                    <div class="tx-amt {color}">{sign}₹{t['amount']:,.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            with row_right:
                if st.button("✕", key=f"del_{t['id']}"):
                    delete_transaction(t["id"])
                    st.rerun()
