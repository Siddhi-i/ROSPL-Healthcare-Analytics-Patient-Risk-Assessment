"""
generate_sample_data.py
------------------------
Generates a synthetic patient dataset for the Healthcare Analytics Dashboard.
Run this once to (re)create data/sample_patient_data.csv

Usage:
    python generate_sample_data.py
"""

import numpy as np
import pandas as pd

np.random.seed(42)

N = 500  # number of synthetic patients

genders = np.random.choice(["Male", "Female"], size=N, p=[0.49, 0.51])

# Age: skew towards adult/older population, typical of hospital records
ages = np.clip(np.random.normal(45, 18, N), 1, 95).astype(int)

# BMI: normal distribution centered slightly above healthy range
bmi = np.clip(np.random.normal(26, 5, N), 14, 48).round(1)

# Blood pressure: correlated loosely with age and BMI
systolic = np.clip(
    100 + (ages * 0.3) + (bmi * 0.5) + np.random.normal(0, 8, N), 90, 200
).astype(int)
diastolic = np.clip(
    60 + (ages * 0.15) + (bmi * 0.3) + np.random.normal(0, 6, N), 55, 130
).astype(int)

diseases = np.random.choice(
    [
        "Hypertension",
        "Diabetes",
        "Asthma",
        "Cardiac Disease",
        "Obesity",
        "Arthritis",
        "None",
        "Thyroid Disorder",
    ],
    size=N,
    p=[0.18, 0.15, 0.10, 0.10, 0.12, 0.10, 0.15, 0.10],
)

notes_pool = {
    "Hypertension": [
        "Patient reports occasional headaches and dizziness, blood pressure elevated.",
        "Feeling stressed at work, BP slightly high but manageable with medication.",
        "Follow-up visit, blood pressure under control, patient feels good.",
    ],
    "Diabetes": [
        "Blood sugar levels fluctuating, patient feels tired and thirsty often.",
        "Patient is managing diet well, glucose levels improving steadily.",
        "Struggling with sugar control, feeling anxious about complications.",
    ],
    "Asthma": [
        "Mild wheezing reported during exercise, otherwise breathing fine.",
        "Patient had a bad asthma attack last week, feeling worried.",
        "Symptoms well controlled with inhaler, patient feels confident.",
    ],
    "Cardiac Disease": [
        "Patient reports chest discomfort, feeling scared about heart health.",
        "Recovering well after treatment, feeling optimistic and relieved.",
        "Routine checkup, heart function stable, patient feels reassured.",
    ],
    "Obesity": [
        "Patient motivated to start new diet plan, feeling hopeful about progress.",
        "Struggling with weight loss, feeling frustrated and discouraged.",
        "Steady progress with exercise routine, patient feels great.",
    ],
    "Arthritis": [
        "Joint pain worsened this week, patient feels uncomfortable and tired.",
        "Pain manageable with medication, patient feels okay overall.",
        "Great improvement in mobility, patient feels happy and relieved.",
    ],
    "None": [
        "Routine annual checkup, patient feels healthy and energetic.",
        "No complaints, patient feels great and active.",
        "General wellness visit, patient is in excellent condition.",
    ],
    "Thyroid Disorder": [
        "Patient feels fatigued and low energy, thyroid levels being monitored.",
        "Medication adjusted, patient feels more energetic this month.",
        "Follow-up shows stable levels, patient feels satisfied.",
    ],
}

notes = [np.random.choice(notes_pool[d]) for d in diseases]

df = pd.DataFrame(
    {
        "PatientID": [f"P{1000+i}" for i in range(N)],
        "Age": ages,
        "Gender": genders,
        "BMI": bmi,
        "Systolic_BP": systolic,
        "Diastolic_BP": diastolic,
        "Disease": diseases,
        "Notes": notes,
    }
)

df.to_csv("data/sample_patient_data.csv", index=False)
print(f"Generated {N} synthetic patient records -> data/sample_patient_data.csv")
