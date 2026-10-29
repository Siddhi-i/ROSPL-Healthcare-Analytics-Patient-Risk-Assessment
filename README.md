# 🏥 Healthcare Analytics Dashboard

An interactive **Streamlit + Plotly** dashboard for analyzing patient healthcare data, with a bonus **TextBlob** sentiment-analysis feature on patient clinical notes.

---

## ✨ Original Project Features

- **Patient Data Upload** — upload your own CSV/Excel file, or use the built-in sample dataset (500 synthetic patients)
- **Age Distribution** — histogram, age-group pie chart, summary statistics
- **Disease Distribution** — frequency bar chart, share-of-total pie chart, disease-by-gender breakdown
- **BMI Analysis** — distribution by category (Underweight/Normal/Overweight/Obese), BMI vs Age bubble chart
- **Blood Pressure Analysis** — systolic vs diastolic scatter plot, BP category classification, box plots
- **Gender Analysis** — gender split, age/BMI/BP comparisons by gender
- **KPI Cards** — total patients, average age, average BMI, average BP, % male, most common condition
- **Bonus: TextBlob Sentiment Analysis** — if your data has a `Notes` column, the dashboard automatically analyzes sentiment (Positive/Neutral/Negative) of clinical notes per disease
- **Sidebar Filters** — filter by age range, gender, and disease across the whole dashboard
- **Download filtered data** as CSV directly from the app

---

## 📁 Project Structure

```text
healthcare_analytics_dashboard/
│
├── app.py
├── generate_sample_data.py
├── requirements.txt
├── README.md
└── data/
    └── sample_patient_data.csv
```

---

## 🧰 Requirements

- **Python 3.13**
- VS Code with the Python extension
- Internet connection for installing dependencies

---

## 🚀 Step-by-Step: Run in VS Code

### 1. Open the project

Open the project folder in VS Code:

```text
File → Open Folder... → select the project folder
```

### 2. Open a terminal

```text
Terminal → New Terminal
```

Make sure the terminal is inside the project folder.

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Generate sample data (optional)

A sample dataset is already included.

To generate a fresh synthetic dataset:

```bash
python generate_sample_data.py
```

### 6. Run the dashboard

```bash
streamlit run app.py
```

### 7. Open the dashboard

Open:

```text
http://localhost:8501
```

### 8. Stop the application

```text
Ctrl + C
```

---

## 📤 Uploading Your Own Data

The dashboard supports CSV and Excel files.

Required columns:

| Column | Type | Example |
|---|---|---|
| PatientID | Text | P1001 |
| Age | Number | 45 |
| Gender | Text | Male / Female |
| BMI | Number | 27.3 |
| Systolic_BP | Number | 132 |
| Diastolic_BP | Number | 84 |
| Disease | Text | Hypertension |
| Notes | Text (optional) | Patient reports mild headache |

If the `Notes` column is present, TextBlob sentiment analysis is automatically performed.

---

## 🛠️ Troubleshooting

### Streamlit command not found

Make sure the virtual environment is activated:

```bash
venv\Scripts\activate
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

### Port already in use

Run:

```bash
streamlit run app.py --server.port 8502
```

### Blank/error page after upload

Check that the uploaded file contains all required columns.

### TextBlob errors

The TextBlob sentiment analyzer used by this project does not require additional NLTK corpus downloads.

---

# 🚀 ROSPL Open Source Contribution

## Project Enhancement: Patient Risk Assessment Module

This project was originally developed as a **Healthcare Analytics Dashboard** using Streamlit, Python, Pandas and Plotly.

As part of the **ROSPL Open Source Mini Project**, the existing open-source project was studied, modified and enhanced with a new **Patient Risk Assessment Module**.

The original dashboard functionality was retained while additional patient-level and population-level risk analytics were integrated.

---

## 🎯 Problem Statement

Healthcare dashboards generally provide descriptive information such as patient demographics, BMI, blood pressure and disease distribution.

However, users may require a consolidated view of patient-level risk indicators to identify patients who may require closer attention.

To address this requirement, a transparent, rule-based **Patient Risk Assessment Module** was integrated into the existing healthcare analytics dashboard.

The module combines available patient attributes such as:

- Age
- BMI
- Blood Pressure
- Existing health conditions

to calculate a project-defined risk score and classify patients into different risk levels.

---

## ✨ Our Contribution

The following functionality was added to the original open-source dashboard:

- 🩺 Patient Risk Assessment module
- 📊 Rule-based patient risk scoring
- 👤 Individual patient assessment
- 🟢 Low Risk classification
- 🟡 Moderate Risk classification
- 🔴 High Risk classification
- 📌 Risk factors based on:
  - Age
  - BMI
  - Blood Pressure
  - Existing health conditions
- 💡 General health recommendations
- 📊 Population-level risk analysis
- Risk analysis by age group
- Risk analysis by gender
- Risk analysis by existing condition
- 📋 Patient risk summary table
- ℹ️ Transparent explanation of the risk-scoring methodology

---

# 🧮 Risk Scoring Methodology

The project uses a transparent, project-defined rule-based scoring mechanism.

## Factors Considered

| Factor | Condition | Score |
|---|---|---:|
| Age | 50–64 years | +1 |
| Age | 65+ years | +2 |
| BMI | Overweight | +1 |
| BMI | Obese | +2 |
| Blood Pressure | Elevated | +1 |
| Blood Pressure | Stage 1 Hypertension | +2 |
| Blood Pressure | Stage 2 Hypertension | +3 |
| Blood Pressure | Hypertensive Crisis | +3 |
| Existing Condition | Recorded condition | +1 |

### Risk Classification

| Risk Score | Risk Level |
|---:|---|
| 0–2 | 🟢 Low |
| 3–4 | 🟡 Moderate |
| 5+ | 🔴 High |

> **Note:** This is a project-defined analytics and screening mechanism intended for educational purposes. It is not a clinical diagnostic or medical prediction model.

---

# 🔄 Project Workflow

```text
Patient Dataset
       ↓
Data Filtering
       ↓
Age + BMI + Blood Pressure + Disease
       ↓
Rule-Based Risk Scoring
       ↓
Risk Classification
       ↓
Individual Patient Assessment
       ↓
General Health Recommendations
       ↓
Population-Level Risk Analysis
       ↓
Patient Risk Summary
```

---

# 👤 Individual Patient Assessment

The enhanced module allows users to select an individual patient and view:

- Age
- BMI
- Blood Pressure
- Risk Score
- Risk Level
- Identified Risk Factors
- General recommendations based on available indicators

Example:

```text
Age: 53
BMI: 28.5
Blood Pressure: 124/76
Risk Score: 4
Risk Level: Moderate
```

The system then provides relevant general recommendations based on the available patient information.

---

# 💡 General Health Recommendations

The module provides general, non-diagnostic recommendations based on identified indicators.

### BMI

- Underweight → general nutrition and healthy weight-management guidance
- Overweight → balanced diet and regular physical activity guidance
- Obese → consideration of professional guidance for sustainable weight management

### Blood Pressure

The system can provide general recommendations for:

- Elevated blood pressure
- Stage 1 hypertension
- Stage 2 hypertension
- Very high blood pressure ranges

### Existing Conditions

When an existing health condition is recorded, the system recommends following the care plan provided by the patient's healthcare professional.

> These recommendations are intended for educational and analytical purposes only and should not be considered medical advice.

---

# 📊 Population Risk Analysis

The enhancement also provides population-level risk analysis.

The risk distribution can be analyzed according to:

### Age Group

Patients can be compared across different age groups to identify the distribution of Low, Moderate and High risk levels.

### Gender

Risk levels can be compared across available gender categories.

### Existing Conditions

The dashboard provides a comparison of risk levels across recorded health conditions.

This allows users to move beyond individual patient assessment and explore patterns in the overall dataset.

---

# 📋 Patient Risk Summary

The enhanced dashboard provides a table containing relevant risk information, including:

- Patient ID
- Age
- Gender
- BMI
- BMI Category
- Systolic Blood Pressure
- Diastolic Blood Pressure
- Blood Pressure Category
- Disease
- Risk Score
- Risk Level
- Risk Factors

---

# 🧪 Testing

The enhanced module was tested using the built-in synthetic patient dataset.

The following functionality was verified:

- Patient risk score generation
- Low, Moderate and High risk classification
- Individual patient selection
- BMI-based recommendations
- Blood-pressure-based recommendations
- Existing-condition identification
- Population-level risk analysis
- Risk analysis by age group
- Risk analysis by gender
- Risk analysis by existing condition
- Risk summary table
- Compatibility with existing dashboard filters

---

# 📸 Proof of Execution

### Original Dashboard

<img width="1909" height="653" alt="Healthcare Analytics Dashboard" src="https://github.com/user-attachments/assets/467851ae-bdaf-4061-aaa7-91c2815e9f93" />

<img width="369" height="901" alt="Healthcare Analytics Dashboard Filters" src="https://github.com/user-attachments/assets/311d3356-289f-4736-9d3d-291fb77e6385" />

<img width="1906" height="920" alt="Healthcare Analytics Dashboard Analysis" src="https://github.com/user-attachments/assets/2ee6312a-e82d-445f-b726-ea8541d3edc7" />

### ROSPL Enhancement

The enhanced dashboard includes:

- Patient Risk Assessment
- Risk distribution charts
- Individual patient assessment
- Risk-based recommendations
- Population-level risk analysis
- Patient risk summary

---

# 🛠️ Technology Stack

### Original Project

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- TextBlob

### ROSPL Enhancement

- Python
- Streamlit
- Pandas
- Plotly
- Git
- GitHub

---

# 📁 Contribution Structure

The primary enhancement was implemented in:

```text
app.py
```

The module was integrated into the existing dashboard without removing the original healthcare analytics functionality.

---

# 🌱 Open Source Contribution

The project was developed by extending an existing open-source Healthcare Analytics Dashboard.

The original dashboard functionality was retained while a new **Patient Risk Assessment layer** was designed and integrated.

The contribution involved:

1. Understanding the existing codebase
2. Identifying an enhancement opportunity
3. Designing a rule-based risk assessment mechanism
4. Integrating the module with the existing Streamlit dashboard
5. Adding individual patient assessment
6. Adding general recommendations
7. Adding population-level risk analytics
8. Testing the enhanced functionality
9. Documenting the contribution

---

# 📝 Contribution Commit

The main enhancement was committed to GitHub with:

```text
Add patient risk assessment module
```

The changes were successfully committed and pushed to the GitHub repository.

---

# ⚠️ Limitations

- The risk score is a **project-defined rule-based mechanism**.
- It is not trained using a clinical dataset.
- It should not be considered a clinical diagnosis or clinical prediction model.
- Recommendations are general and intended only for educational and analytical purposes.
- The current implementation is limited to the available patient attributes.
- The scoring methodology would require validation against appropriate healthcare datasets before any real-world application.

---

# 🔮 Future Scope

The Patient Risk Assessment module can be further enhanced with:

- Machine-learning-based risk prediction using validated healthcare datasets
- Integration with electronic health records
- Additional clinical parameters and laboratory results
- Explainable AI techniques for risk prediction
- Personalized dashboards for healthcare professionals
- Secure patient authentication
- Role-based access control
- Historical patient risk tracking
- Real-time healthcare data integration
- Model validation using clinically approved datasets
- Improved visualization and reporting
- Exportable patient risk reports

---

# 📌 ROSPL Contribution Summary

| Component | Status |
|---|---|
| Existing Healthcare Analytics Dashboard | Open-source base project |
| Patient Risk Assessment | ✅ Added |
| Rule-Based Risk Scoring | ✅ Added |
| Individual Patient Assessment | ✅ Added |
| Risk Classification | ✅ Added |
| General Health Recommendations | ✅ Added |
| Population Risk Analysis | ✅ Added |
| Risk by Age Group | ✅ Added |
| Risk by Gender | ✅ Added |
| Risk by Existing Condition | ✅ Added |
| Patient Risk Summary Table | ✅ Added |
| Risk Methodology Documentation | ✅ Added |
| Testing Documentation | ✅ Added |

---

# ⚖️ Disclaimer

This project is intended for **educational and analytical purposes only**.

The risk score and recommendations generated by this application should **not** be used as a substitute for professional medical advice, diagnosis or treatment.

---

## 📊 Tech Stack

- [Streamlit](https://streamlit.io/) — dashboard framework
- [Plotly](https://plotly.com/python/) — interactive charts
- [Pandas](https://pandas.pydata.org/) / [NumPy](https://numpy.org/) — data processing
- [TextBlob](https://textblob.readthedocs.io/) — sentiment analysis
- Git & GitHub — version control and open-source collaboration

---

## 🎉 Acknowledgement

This project builds upon an existing open-source Healthcare Analytics Dashboard and extends its functionality as part of an academic **ROSPL Open Source Mini Project**.

The enhancement focuses on adding transparent patient risk assessment and population-level risk analytics while retaining the original dashboard capabilities.
