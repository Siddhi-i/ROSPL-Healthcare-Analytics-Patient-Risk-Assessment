"""
Healthcare Analytics Dashboard
------------------------------
A Streamlit + Plotly dashboard for exploring patient health data:
- Patient data upload (CSV/Excel)
- Age distribution
- Disease distribution
- BMI analysis
- Blood pressure analysis
- Gender analysis
- KPI cards
- Bonus: TextBlob sentiment analysis on patient notes (if a 'Notes' column exists)

Run with:
    streamlit run app.py
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from textblob import TextBlob

# --------------------------------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------------------------------
st.set_page_config(
    page_title="Healthcare Analytics Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

PRIMARY_COLOR = "#2E86AB"
ACCENT_COLOR = "#E63946"

# --------------------------------------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------------------------------------
REQUIRED_NUMERIC_COLS = ["Age", "BMI", "Systolic_BP", "Diastolic_BP"]


@st.cache_data
def load_data(file) -> pd.DataFrame:
    if file is None:
        return pd.read_csv("data/sample_patient_data.csv")
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    return pd.read_excel(file)


def bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def bp_category(systolic: float, diastolic: float) -> str:
    if systolic < 120 and diastolic < 80:
        return "Normal"
    elif systolic < 130 and diastolic < 80:
        return "Elevated"
    elif systolic < 140 or diastolic < 90:
        return "Hypertension Stage 1"
    elif systolic < 180 or diastolic < 120:
        return "Hypertension Stage 2"
    else:
        return "Hypertensive Crisis"


def sentiment_label(polarity: float) -> str:
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    return "Neutral"


def kpi_card(col, label, value, delta=None, help_text=None):
    col.metric(label=label, value=value, delta=delta, help=help_text)


# --------------------------------------------------------------------------------
# SIDEBAR — DATA UPLOAD
# --------------------------------------------------------------------------------
st.sidebar.title("🏥 Healthcare Analytics")
st.sidebar.markdown("Upload patient-level data or use the built-in sample dataset.")

uploaded_file = st.sidebar.file_uploader(
    "Upload Patient Data (CSV or Excel)", type=["csv", "xlsx", "xls"]
)

if uploaded_file:
    st.sidebar.success(f"Loaded: {uploaded_file.name}")
else:
    st.sidebar.info("No file uploaded — showing sample dataset (500 synthetic patients).")

df = load_data(uploaded_file)

# Validate required columns
missing_cols = [c for c in REQUIRED_NUMERIC_COLS + ["Gender", "Disease"] if c not in df.columns]
if missing_cols:
    st.error(
        f"The uploaded file is missing required column(s): {', '.join(missing_cols)}.\n\n"
        f"Expected columns: PatientID, Age, Gender, BMI, Systolic_BP, Diastolic_BP, Disease, "
        f"(optional) Notes"
    )
    st.stop()

# Derived columns
df["BMI_Category"] = df["BMI"].apply(bmi_category)
df["BP_Category"] = df.apply(lambda r: bp_category(r["Systolic_BP"], r["Diastolic_BP"]), axis=1)
has_notes = "Notes" in df.columns and df["Notes"].notna().any()
if has_notes:
    df["Sentiment_Polarity"] = df["Notes"].astype(str).apply(lambda t: TextBlob(t).sentiment.polarity)
    df["Sentiment"] = df["Sentiment_Polarity"].apply(sentiment_label)

# --------------------------------------------------------------------------------
# SIDEBAR — FILTERS
# --------------------------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("Filters")

age_min, age_max = int(df["Age"].min()), int(df["Age"].max())
age_range = st.sidebar.slider("Age Range", age_min, age_max, (age_min, age_max))

gender_options = sorted(df["Gender"].dropna().unique().tolist())
selected_genders = st.sidebar.multiselect("Gender", gender_options, default=gender_options)

disease_options = sorted(df["Disease"].dropna().unique().tolist())
selected_diseases = st.sidebar.multiselect("Disease", disease_options, default=disease_options)

filtered_df = df[
    (df["Age"].between(age_range[0], age_range[1]))
    & (df["Gender"].isin(selected_genders))
    & (df["Disease"].isin(selected_diseases))
]

if filtered_df.empty:
    st.warning("No records match the selected filters. Please adjust the filters in the sidebar.")
    st.stop()

# --------------------------------------------------------------------------------
# HEADER
# --------------------------------------------------------------------------------
st.title("🏥 Healthcare Analytics Dashboard")
st.caption("Interactive patient population insights — upload your own data or explore the sample dataset.")

# --------------------------------------------------------------------------------
# KPI CARDS
# --------------------------------------------------------------------------------
st.markdown("### 📌 Key Performance Indicators")
k1, k2, k3, k4, k5, k6 = st.columns(6)

kpi_card(k1, "Total Patients", f"{len(filtered_df):,}")
kpi_card(k2, "Avg. Age", f"{filtered_df['Age'].mean():.1f} yrs")
kpi_card(k3, "Avg. BMI", f"{filtered_df['BMI'].mean():.1f}")
kpi_card(
    k4,
    "Avg. BP",
    f"{filtered_df['Systolic_BP'].mean():.0f}/{filtered_df['Diastolic_BP'].mean():.0f}",
)
male_pct = (filtered_df["Gender"] == "Male").mean() * 100 if "Male" in gender_options else 0
kpi_card(k5, "% Male", f"{male_pct:.1f}%")
most_common_disease = filtered_df["Disease"].mode()[0]
kpi_card(k6, "Top Condition", most_common_disease)

st.markdown("---")

# --------------------------------------------------------------------------------
# TABS
# --------------------------------------------------------------------------------
tab_age, tab_disease,tab_bmi,tab_bp, tab_gender, tab_risk,tab_data = st.tabs(
    [
        "📊 Age Distribution",
        "🦠 Disease Distribution",
        "⚖️ BMI Analysis",
        "❤️ Blood Pressure",
        "🚻 Gender Analysis",
        "🩺 Patient Risk Assessment",
        "📄 Raw Data",
    ]
)

# ---------------- AGE DISTRIBUTION ----------------
with tab_age:
    st.subheader("Age Distribution")
    c1, c2 = st.columns([2, 1])
    with c1:
        fig = px.histogram(
            filtered_df,
            x="Age",
            nbins=20,
            color_discrete_sequence=[PRIMARY_COLOR],
            marginal="box",
            title="Patient Age Distribution",
        )
        fig.update_layout(bargap=0.05)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        bins = [0, 18, 35, 50, 65, 120]
        labels = ["0-17", "18-34", "35-49", "50-64", "65+"]
        age_group = pd.cut(filtered_df["Age"], bins=bins, labels=labels, right=False)
        age_group_counts = age_group.value_counts().sort_index()
        fig2 = px.pie(
            values=age_group_counts.values,
            names=age_group_counts.index,
            title="Age Group Breakdown",
            hole=0.45,
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("**Age Statistics**")
    st.dataframe(filtered_df["Age"].describe().to_frame().T, use_container_width=True)

# ---------------- DISEASE DISTRIBUTION ----------------
with tab_disease:
    st.subheader("Disease Distribution")
    disease_counts = filtered_df["Disease"].value_counts().reset_index()
    disease_counts.columns = ["Disease", "Count"]

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(
            disease_counts,
            x="Count",
            y="Disease",
            orientation="h",
            color="Count",
            color_continuous_scale="Blues",
            title="Disease Frequency",
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = px.pie(disease_counts, values="Count", names="Disease", title="Disease Share (%)")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("**Disease vs Gender Breakdown**")
    cross = pd.crosstab(filtered_df["Disease"], filtered_df["Gender"])
    fig3 = px.bar(cross, barmode="group", title="Disease Cases by Gender")
    st.plotly_chart(fig3, use_container_width=True)

    if has_notes:
        st.markdown("**🧠 Patient Notes Sentiment (via TextBlob)**")
        sc1, sc2 = st.columns([1, 2])
        with sc1:
            sentiment_counts = filtered_df["Sentiment"].value_counts().reset_index()
            sentiment_counts.columns = ["Sentiment", "Count"]
            fig4 = px.pie(
                sentiment_counts,
                values="Count",
                names="Sentiment",
                title="Overall Note Sentiment",
                color="Sentiment",
                color_discrete_map={"Positive": "#2ECC71", "Neutral": "#95A5A6", "Negative": "#E74C3C"},
            )
            st.plotly_chart(fig4, use_container_width=True)
        with sc2:
            fig5 = px.box(
                filtered_df,
                x="Disease",
                y="Sentiment_Polarity",
                color="Disease",
                title="Sentiment Polarity by Disease",
                points=False,
            )
            fig5.update_layout(showlegend=False)
            st.plotly_chart(fig5, use_container_width=True)

# ---------------- BMI ANALYSIS ----------------
with tab_bmi:
    st.subheader("BMI Analysis")
    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(
            filtered_df,
            x="BMI",
            nbins=25,
            color="BMI_Category",
            title="BMI Distribution by Category",
            category_orders={"BMI_Category": ["Underweight", "Normal", "Overweight", "Obese"]},
        )
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        bmi_cat_counts = filtered_df["BMI_Category"].value_counts().reset_index()
        bmi_cat_counts.columns = ["Category", "Count"]
        fig2 = px.pie(bmi_cat_counts, values="Count", names="Category", title="BMI Category Share", hole=0.4)
        st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.scatter(
        filtered_df,
        x="Age",
        y="BMI",
        color="BMI_Category",
        size="Systolic_BP",
        hover_data=["Gender", "Disease"],
        title="BMI vs Age (bubble size = Systolic BP)",
    )
    st.plotly_chart(fig3, use_container_width=True)

# ---------------- BLOOD PRESSURE ----------------
with tab_bp:
    st.subheader("Blood Pressure Analysis")
    c1, c2 = st.columns(2)
    with c1:
        fig = px.scatter(
            filtered_df,
            x="Systolic_BP",
            y="Diastolic_BP",
            color="BP_Category",
            hover_data=["Age", "Gender", "Disease"],
            title="Systolic vs Diastolic BP",
        )
        fig.add_shape(
            type="line", x0=120, x1=120, y0=filtered_df["Diastolic_BP"].min(),
            y1=filtered_df["Diastolic_BP"].max(), line=dict(dash="dash", color="gray"),
        )
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        bp_cat_counts = filtered_df["BP_Category"].value_counts().reset_index()
        bp_cat_counts.columns = ["Category", "Count"]
        fig2 = px.bar(
            bp_cat_counts,
            x="Category",
            y="Count",
            color="Category",
            title="Blood Pressure Category Distribution",
        )
        st.plotly_chart(fig2, use_container_width=True)

    fig3 = go.Figure()
    fig3.add_trace(go.Box(y=filtered_df["Systolic_BP"], name="Systolic", marker_color=PRIMARY_COLOR))
    fig3.add_trace(go.Box(y=filtered_df["Diastolic_BP"], name="Diastolic", marker_color=ACCENT_COLOR))
    fig3.update_layout(title="Systolic vs Diastolic BP Spread")
    st.plotly_chart(fig3, use_container_width=True)

# ---------------- GENDER ANALYSIS ----------------
with tab_gender:
    st.subheader("Gender Analysis")
    c1, c2 = st.columns(2)
    with c1:
        gender_counts = filtered_df["Gender"].value_counts().reset_index()
        gender_counts.columns = ["Gender", "Count"]
        fig = px.pie(gender_counts, values="Count", names="Gender", title="Gender Split", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = px.box(
            filtered_df, x="Gender", y="Age", color="Gender", title="Age Distribution by Gender"
        )
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        fig3 = px.violin(
            filtered_df, x="Gender", y="BMI", color="Gender", box=True, title="BMI Distribution by Gender"
        )
        st.plotly_chart(fig3, use_container_width=True)
    with c4:
        avg_bp_gender = filtered_df.groupby("Gender")[["Systolic_BP", "Diastolic_BP"]].mean().reset_index()
        fig4 = px.bar(
            avg_bp_gender,
            x="Gender",
            y=["Systolic_BP", "Diastolic_BP"],
            barmode="group",
            title="Average Blood Pressure by Gender",
        )
        st.plotly_chart(fig4, use_container_width=True)

# ---------------- PATIENT RISK ASSESSMENT ----------------
with tab_risk:
    st.subheader("🩺 Patient Risk Assessment")
    st.caption(
          "A transparent rule-based screening score using age, BMI, blood pressure, "
    "and recorded health conditions. This is for analytics and educational "
    "purposes only and is not a medical diagnosis."
)
with st.expander("ℹ️ How is the risk score calculated?"):
    st.markdown("""
    **Risk factors considered:**

    - **Age:** Higher scores for older age groups.
    - **BMI:** Additional points for overweight or obese categories.
    - **Blood Pressure:** Points increase with the BP category.
    - **Existing Condition:** An additional point is assigned when a recorded
      health condition is present.

    **Risk interpretation:**

    - 🟢 **Low Risk:** Score below 3
    - 🟡 **Moderate Risk:** Score 3–4
    - 🔴 **High Risk:** Score 5 or above

    This scoring system is a project-defined rule-based screening mechanism
    and should not be interpreted as a clinical risk prediction model.
    """)

    # Work on a copy so the original filtered dataset remains unchanged
    risk_df = filtered_df.copy()

    # Create a transparent risk score
    def calculate_risk(row):
        score = 0
        factors = []

        # Age factor
        if row["Age"] >= 65:
            score += 2
            factors.append("Age ≥ 65")
        elif row["Age"] >= 50:
            score += 1
            factors.append("Age 50–64")

        # BMI factor
        if row["BMI_Category"] == "Obese":
            score += 2
            factors.append("Obese BMI")
        elif row["BMI_Category"] == "Overweight":
            score += 1
            factors.append("Overweight BMI")

        # Blood pressure factor
        if row["BP_Category"] == "Hypertensive Crisis":
            score += 3
            factors.append("Hypertensive Crisis")
        elif row["BP_Category"] == "Hypertension Stage 2":
            score += 3
            factors.append("Stage 2 Hypertension")
        elif row["BP_Category"] == "Hypertension Stage 1":
            score += 2
            factors.append("Stage 1 Hypertension")
        elif row["BP_Category"] == "Elevated":
            score += 1
            factors.append("Elevated BP")

        # Disease factor
        disease = str(row["Disease"]).strip().lower()
        if disease not in ["none", "no disease", "healthy", "nan", ""]:
            score += 1
            factors.append("Existing condition")

        # Convert score into risk category
        if score >= 5:
            risk = "High"
        elif score >= 3:
            risk = "Moderate"
        else:
            risk = "Low"

        return pd.Series([score, risk, ", ".join(factors) if factors else "No major risk factors"])

    risk_df[["Risk_Score", "Risk_Level", "Risk_Factors"]] = risk_df.apply(
        calculate_risk, axis=1
    )

    # ---------------- RISK KPIs ----------------
    st.markdown("### 📌 Risk Overview")

    r1, r2, r3, r4 = st.columns(4)

    total_risk_patients = len(risk_df)
    low_count = (risk_df["Risk_Level"] == "Low").sum()
    moderate_count = (risk_df["Risk_Level"] == "Moderate").sum()
    high_count = (risk_df["Risk_Level"] == "High").sum()

    r1.metric("Patients Assessed", total_risk_patients)
    r2.metric("Low Risk", low_count)
    r3.metric("Moderate Risk", moderate_count)
    r4.metric("High Risk", high_count)

    st.markdown("---")

    # ---------------- RISK DISTRIBUTION ----------------
    c1, c2 = st.columns(2)

    with c1:
        risk_counts = (
            risk_df["Risk_Level"]
            .value_counts()
            .reindex(["Low", "Moderate", "High"], fill_value=0)
            .reset_index()
        )
        risk_counts.columns = ["Risk Level", "Count"]

        fig_risk = px.bar(
            risk_counts,
            x="Risk Level",
            y="Count",
            color="Risk Level",
            title="Patient Risk Distribution",
        )

        st.plotly_chart(fig_risk, use_container_width=True)

    with c2:
        fig_risk_pie = px.pie(
            risk_counts,
            values="Count",
            names="Risk Level",
            title="Risk Level Share",
            hole=0.45,
        )

        st.plotly_chart(fig_risk_pie, use_container_width=True)

    # ---------------- PATIENT SELECTION ----------------
    st.markdown("### 👤 Individual Patient Assessment")

    if "PatientID" in risk_df.columns:
        patient_options = risk_df["PatientID"].astype(str).tolist()
        selected_patient = st.selectbox(
            "Select a Patient",
            patient_options
        )

        selected_row = risk_df[
            risk_df["PatientID"].astype(str) == selected_patient
        ].iloc[0]
    else:
        patient_options = risk_df.index.tolist()
        selected_patient = st.selectbox(
            "Select Patient Record",
            patient_options
        )

        selected_row = risk_df.loc[selected_patient]

    p1, p2, p3, p4 = st.columns(4)

    p1.metric("Age", f"{selected_row['Age']:.0f}")
    p2.metric("BMI", f"{selected_row['BMI']:.1f}")
    p3.metric(
        "Blood Pressure",
        f"{selected_row['Systolic_BP']:.0f}/{selected_row['Diastolic_BP']:.0f}"
    )
    p4.metric("Risk Score", f"{selected_row['Risk_Score']:.0f}")

    st.markdown("#### Risk Result")

    risk_level = selected_row["Risk_Level"]

    if risk_level == "High":
        st.error(f"🔴 **Risk Level: {risk_level}**")
    elif risk_level == "Moderate":
        st.warning(f"🟡 **Risk Level: {risk_level}**")
    else:
        st.success(f"🟢 **Risk Level: {risk_level}**")

    st.info(
        f"**Risk Factors:** {selected_row['Risk_Factors']}"
    )

    # ---------------- RISK-BASED RECOMMENDATIONS ----------------
    st.markdown("### 💡 General Health Recommendations")

    bmi_category = selected_row["BMI_Category"]
    bp_category = selected_row["BP_Category"]

    # Overall risk message
    if risk_level == "High":
        st.error(
            "🔴 **High Risk:** Multiple health indicators require attention. "
            "Professional medical evaluation is recommended."
        )

    elif risk_level == "Moderate":
        st.warning(
            "🟡 **Moderate Risk:** Some health indicators require attention. "
            "Consider improving lifestyle habits and monitoring your health regularly."
        )

    else:
        st.success(
            "🟢 **Low Risk:** No major risk indicators were detected based on "
            "the available information. Continue healthy lifestyle habits."
        )

    # ---------------- SUGGESTED ACTIONS ----------------
    st.markdown("#### 💡 Suggested Actions")

    if bmi_category == "Obese":
        st.info(
            "💡 **BMI:** Your BMI falls in the obese category. "
            "Consider professional guidance for sustainable weight management."
        )

    elif bmi_category == "Overweight":
        st.info(
            "💡 **BMI:** Your BMI falls in the overweight category. "
            "A balanced diet and regular physical activity may be beneficial."
        )

    elif bmi_category == "Underweight":
        st.info(
            "💡 **BMI:** Your BMI falls in the underweight category. "
            "Consider discussing healthy nutrition and weight management "
            "with a healthcare professional."
        )

    # Blood pressure recommendations
    if bp_category == "Elevated":
        st.info(
            "💡 **Blood Pressure:** Blood pressure is elevated. "
            "Regular monitoring and healthy lifestyle habits may be beneficial."
        )

    elif bp_category == "Hypertension Stage 1":
        st.info(
            "💡 **Blood Pressure:** Blood pressure falls in Stage 1 hypertension. "
            "Regular monitoring and professional medical advice are recommended."
        )

    elif bp_category == "Hypertension Stage 2":
        st.info(
            "💡 **Blood Pressure:** Blood pressure falls in Stage 2 hypertension. "
            "Medical evaluation and regular monitoring are recommended."
        )

    elif bp_category == "Hypertensive Crisis":
        st.error(
            "🚨 **Blood Pressure:** Blood pressure is in a very high range. "
            "Prompt medical attention is recommended, especially if symptoms "
            "are present."
        )

    # Existing condition recommendation
    disease = str(selected_row["Disease"]).strip().lower()

    if disease not in ["none", "no disease", "healthy", "nan", ""]:
        st.info(
            "💡 **Existing Condition:** A health condition is recorded. "
            "Follow the care plan provided by the patient's healthcare professional."
        )

    # Age recommendation
    if selected_row["Age"] >= 65:
        st.info(
            "💡 **Age:** Regular health monitoring is advisable for older adults."
        )

    # ---------------- RISK TABLE ----------------
    st.markdown("### 📋 Patient Risk Summary")

    display_columns = []

    for col in [
        "PatientID",
        "Age",
        "Gender",
        "BMI",
        "BMI_Category",
        "Systolic_BP",
        "Diastolic_BP",
        "BP_Category",
        "Disease",
        "Risk_Score",
        "Risk_Level",
        "Risk_Factors",
    ]:
        if col in risk_df.columns:
            display_columns.append(col)

    st.dataframe(
        risk_df[display_columns],
        use_container_width=True,
        hide_index=True,
    )
# ---------------- RAW DATA ----------------
with tab_data:
    st.subheader("Filtered Patient Data")
    st.dataframe(filtered_df, use_container_width=True)
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_patient_data.csv",
        mime="text/csv",
    )

st.markdown("---")
st.caption("Built with Streamlit + Plotly + TextBlob | Healthcare Analytics Dashboard")
