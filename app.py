import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="SmartLoan AI",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------- Styling ----------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #eef7ff 0%, #f8f3ff 48%, #effff7 100%);
    }
    .main-title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        color: #173b75;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        color: #5b6b82;
        font-size: 17px;
        margin-bottom: 25px;
    }
    .hero {
        background: linear-gradient(120deg, #2563eb, #7c3aed);
        padding: 24px;
        border-radius: 20px;
        color: white;
        margin-bottom: 22px;
        box-shadow: 0 10px 30px rgba(37,99,235,.20);
    }
    .hero h2 { margin: 0 0 8px 0; color: white; }
    .hero p { margin: 0; opacity: .95; }
    .card {
        background: white;
        padding: 18px;
        border-radius: 16px;
        border: 1px solid #e6edf7;
        box-shadow: 0 5px 18px rgba(20,50,90,.07);
        margin: 10px 0;
    }
    .approved {
        background: linear-gradient(135deg, #dcfce7, #ecfdf5);
        border-left: 7px solid #16a34a;
        padding: 20px;
        border-radius: 16px;
        margin-top: 18px;
    }
    .rejected {
        background: linear-gradient(135deg, #fee2e2, #fff1f2);
        border-left: 7px solid #dc2626;
        padding: 20px;
        border-radius: 16px;
        margin-top: 18px;
    }
    .review {
        background: linear-gradient(135deg, #fef3c7, #fffbeb);
        border-left: 7px solid #d97706;
        padding: 20px;
        border-radius: 16px;
        margin-top: 18px;
    }
    .metric-box {
        background: #ffffff;
        border-radius: 14px;
        padding: 14px;
        text-align: center;
        border: 1px solid #e5e7eb;
    }
    .small-label {
        color: #64748b;
        font-size: 13px;
    }
    .big-value {
        color: #173b75;
        font-size: 23px;
        font-weight: 750;
    }
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 50px;
        font-weight: 700;
        font-size: 17px;
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        color: white;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Agent 1 ----------
def credit_agent(credit_score, monthly_income, existing_emi, defaults):
    """Agent 1: evaluates basic credit risk."""
    if defaults > 0:
        risk = "High"
        reason = "Active payment defaults were reported."
    elif credit_score >= 750:
        risk = "Low"
        reason = "Excellent credit score."
    elif credit_score >= 700:
        risk = "Low"
        reason = "Good credit score."
    elif credit_score >= 650:
        risk = "Medium"
        reason = "Credit score is acceptable but requires additional review."
    else:
        risk = "High"
        reason = "Credit score is below the minimum preferred range."

    debt_ratio = existing_emi / monthly_income if monthly_income else 1

    return {
        "risk": risk,
        "reason": reason,
        "debt_ratio": debt_ratio,
        "score": credit_score,
    }

# ---------- Agent 2 ----------
def loan_decision_agent(credit_result, monthly_income, loan_amount, employment_years):
    """Agent 2: combines credit and affordability information."""
    max_emi_ratio = 0.40
    estimated_emi = loan_amount / 60  # simple 5-year principal approximation
    current_ratio = (
        (estimated_emi + monthly_income * credit_result["debt_ratio"])
        / monthly_income
    )

    if credit_result["risk"] == "High":
        decision = "REJECTED"
        explanation = "The application has a high credit risk."
    elif employment_years < 1:
        decision = "REVIEW"
        explanation = "Employment history is less than one year."
    elif current_ratio > max_emi_ratio:
        decision = "REVIEW"
        explanation = "Estimated total monthly obligation is relatively high."
    else:
        decision = "APPROVED"
        explanation = "Credit risk and affordability are within the basic criteria."

    return {
        "decision": decision,
        "estimated_emi": estimated_emi,
        "affordability_ratio": current_ratio,
        "explanation": explanation,
    }

# ---------- Header ----------
st.markdown('<div class="main-title">🏦 SmartLoan AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Simple AI-powered loan pre-approval assistant</div>',
    unsafe_allow_html=True,
)

st.markdown("""
<div class="hero">
    <h2>✨ Get your preliminary loan decision</h2>
    <p>Two AI agents evaluate credit risk and affordability in seconds.</p>
</div>
""", unsafe_allow_html=True)

# ---------- Customer form ----------
st.markdown("### 👤 Customer Information")

with st.form("loan_form"):
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full Name", placeholder="Enter your name")
        age = st.number_input("Age", min_value=18, max_value=75, value=30)
        monthly_income = st.number_input(
            "Monthly Income (₹)", min_value=10000, max_value=10000000,
            value=80000, step=5000
        )
        employment_years = st.number_input(
            "Employment Experience (years)", min_value=0.0, max_value=50.0,
            value=3.0, step=0.5
        )

    with col2:
        credit_score = st.number_input(
            "CIBIL / Credit Score", min_value=300, max_value=900,
            value=742, step=1
        )
        existing_emi = st.number_input(
            "Existing Monthly EMI (₹)", min_value=0, max_value=5000000,
            value=10000, step=1000
        )
        loan_amount = st.number_input(
            "Requested Loan Amount (₹)", min_value=50000, max_value=10000000,
            value=500000, step=50000
        )
        defaults = st.number_input(
            "Payment Defaults", min_value=0, max_value=20, value=0, step=1
        )

    submitted = st.form_submit_button("🚀 Check Loan Eligibility")

# ---------- Processing ----------
if submitted:
    if not name.strip():
        st.error("Please enter your name.")
        st.stop()

    if existing_emi >= monthly_income:
        st.warning("Existing EMI is equal to or greater than monthly income. Please verify the values.")

    with st.spinner("🤖 Agent 1 is checking credit risk..."):
        credit_result = credit_agent(
            credit_score, monthly_income, existing_emi, defaults
        )

    with st.spinner("🤖 Agent 2 is checking affordability and making a decision..."):
        decision_result = loan_decision_agent(
            credit_result, monthly_income, loan_amount, employment_years
        )

    # Persist result so it remains visible after the form submission.
    st.session_state["loan_result"] = {
        "name": name,
        "age": age,
        "credit": credit_result,
        "decision": decision_result,
        "loan_amount": loan_amount,
        "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
    }

# ---------- Persistent result ----------
if "loan_result" in st.session_state:
    result = st.session_state["loan_result"]
    credit = result["credit"]
    decision = result["decision"]

    st.markdown("---")
    st.markdown("### 📋 Loan Assessment")

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(
            f'<div class="metric-box"><div class="small-label">Customer</div>'
            f'<div class="big-value">{result["name"]}</div></div>',
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            f'<div class="metric-box"><div class="small-label">Credit Score</div>'
            f'<div class="big-value">{credit["score"]}</div></div>',
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            f'<div class="metric-box"><div class="small-label">Credit Risk</div>'
            f'<div class="big-value">{credit["risk"]}</div></div>',
            unsafe_allow_html=True,
        )
    with m4:
        st.markdown(
            f'<div class="metric-box"><div class="small-label">Requested</div>'
            f'<div class="big-value">₹{result["loan_amount"]:,.0f}</div></div>',
            unsafe_allow_html=True,
        )

    if decision["decision"] == "APPROVED":
        st.markdown(
            f"""
            <div class="approved">
                <h2>✅ Loan Pre-Approved</h2>
                <p><b>Customer:</b> {result["name"]}</p>
                <p><b>Reason:</b> {decision["explanation"]}</p>
                <p><b>Estimated EMI:</b> ₹{decision["estimated_emi"]:,.0f} / month</p>
                <p><b>Assessment time:</b> {result["timestamp"]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.success("🎉 Congratulations! Your application meets the basic pre-approval criteria.")

    elif decision["decision"] == "REVIEW":
        st.markdown(
            f"""
            <div class="review">
                <h2>🟠 Manual Review Recommended</h2>
                <p><b>Customer:</b> {result["name"]}</p>
                <p><b>Reason:</b> {decision["explanation"]}</p>
                <p><b>Estimated EMI:</b> ₹{decision["estimated_emi"]:,.0f} / month</p>
                <p>Your application should be reviewed by a loan officer before a final decision.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        st.markdown(
            f"""
            <div class="rejected">
                <h2>❌ Loan Not Approved</h2>
                <p><b>Customer:</b> {result["name"]}</p>
                <p><b>Reason:</b> {decision["explanation"]}</p>
                <p>You may improve your credit profile and apply again later.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with st.expander("🔍 See AI Agent Details"):
        st.write("**Agent 1 — Credit Risk Agent**")
        st.json(credit)
        st.write("**Agent 2 — Loan Decision Agent**")
        st.json(decision)

st.markdown("---")
st.caption("Demo application for educational/interview purposes. This is not a real banking credit decision.")
