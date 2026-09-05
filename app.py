import streamlit as st
import pandas as pd
import joblib


# --------------------------------------------------
# Load trained model
# --------------------------------------------------

model = joblib.load("fraud_detection_model.pkl")


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="🛡️",
    layout="centered"
)

# --------------------------------------------------
# Load CSS
# --------------------------------------------------

with open("style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    """
    <div class="app-header">
        <div class="badge">🛡️ AI-Powered</div>
        <h1>Transaction Fraud Detection</h1>
        <p>Enter transaction details below and let the model score the risk of fraud in real time.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Merchant details
# --------------------------------------------------

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🏬 Merchant Details</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    merchant_category = st.selectbox(
        "Merchant Category",
        [
            "Restaurant",
            "Entertainment",
            "Grocery",
            "Gas",
            "Healthcare",
            "Travel",
            "Retail",
            "Electronics"
        ]
    )
    merchant = st.text_input(
        "Merchant",
        placeholder="e.g. Taco Bell"
    )
with col2:
    merchant_type = st.selectbox(
        "Merchant Type",
        [
            "fast_food",
            "gaming",
            "physical",
            "major",
            "medical",
            "online"
        ]
    )
    high_risk_merchant = st.selectbox(
        "High Risk Merchant",
        [True, False]
    )
st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# Transaction details
# --------------------------------------------------

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">💳 Transaction Details</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    amount = st.number_input(
        "Transaction Amount",
        min_value=0.0,
        value=100.0,
        step=1.0
    )
    card_type = st.selectbox(
        "Card Type",
        ["credit", "debit"]
    )
    device = st.selectbox(
        "Device",
        ["Chrome", "Firefox", "Edge", "Safari", "iOS App", "Android App"]
    )
with col2:
    currency = st.selectbox(
        "Currency",
        ["USD", "EUR", "GBP", "INR", "JPY", "AUD", "BRL", "NGN"]
    )
    card_present = st.selectbox(
        "Card Present",
        [True, False]
    )
    channel = st.selectbox(
        "Channel",
        ["web", "mobile", "ATM", "POS"]
    )
st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# Location details
# --------------------------------------------------

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📍 Location</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    country = st.text_input(
        "Country",
        placeholder="e.g. India"
    )
    city_size = st.selectbox(
        "City Size",
        ["small", "medium", "large"]
    )
with col2:
    city = st.text_input(
        "City",
        placeholder="e.g. Jalandhar"
    )
    distance_from_home = st.number_input(
        "Distance From Home",
        min_value=0,
        value=0,
        step=1
    )
st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# Timing & velocity
# --------------------------------------------------

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">⏱️ Timing &amp; Velocity</div>', unsafe_allow_html=True)

transaction_hour = st.slider(
    "Transaction Hour",
    min_value=0,
    max_value=23,
    value=12
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    year = st.number_input("Year", min_value=2020, max_value=2030, value=2024, step=1)
with col2:
    month = st.number_input("Month", min_value=1, max_value=12, value=1, step=1)
with col3:
    day = st.number_input("Day", min_value=1, max_value=31, value=1, step=1)
with col4:
    day_of_week = st.number_input("Day of Week", min_value=0, max_value=6, value=0, step=1)

col1, col2, col3 = st.columns(3)
with col1:
    weekend_transaction = st.selectbox("Weekend Transaction", [True, False])
with col2:
    velocity_transactions = st.number_input(
        "Transactions (Last Hour)",
        min_value=0,
        value=1,
        step=1
    )
with col3:
    velocity_amount = st.number_input(
        "Amount (Last Hour)",
        min_value=0.0,
        value=100.0,
        step=1.0
    )
st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# Prediction
# --------------------------------------------------

predict_clicked = st.button("🔍 Predict Fraud")

if predict_clicked:

    input_data = pd.DataFrame({
        "merchant_category": [merchant_category],
        "merchant_type": [merchant_type],
        "merchant": [merchant],
        "amount": [amount],
        "currency": [currency],
        "country": [country],
        "city": [city],
        "city_size": [city_size],
        "card_type": [card_type],
        "card_present": [card_present],
        "device": [device],
        "channel": [channel],
        "distance_from_home": [distance_from_home],
        "high_risk_merchant": [high_risk_merchant],
        "transaction_hour": [transaction_hour],
        "weekend_transaction": [weekend_transaction],
        "velocity_transactions": [velocity_transactions],
        "velocity_amount": [velocity_amount],
        "year": [year],
        "month": [month],
        "day": [day],
        "day_of_week": [day_of_week]
    })

    # Make prediction
    prediction = model.predict(input_data)[0]

    # Get fraud probability
    probability = model.predict_proba(input_data)[0][1]

    st.divider()

    if prediction == 1:
        st.markdown(
            f"""
            <div class="prediction-box prediction-fraud">
                <div class="result-icon">🚨</div>
                <div class="result-title" style="color:#f87171;">Fraudulent Transaction Detected</div>
                <div class="result-sub">This transaction shows strong signals of fraud</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div class="prediction-box prediction-safe">
                <div class="result-icon">✅</div>
                <div class="result-title" style="color:#34d399;">Legitimate Transaction</div>
                <div class="result-sub">No significant fraud signals detected</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    m1, m2 = st.columns(2)
    with m1:
        st.metric("Fraud Probability", f"{probability * 100:.2f}%")
    with m2:
        st.metric("Model Verdict", "Fraud" if prediction == 1 else "Legitimate")

st.markdown(
    '<div class="footer-note">Powered by a machine learning fraud model · For demonstration purposes only</div>',
    unsafe_allow_html=True
)
