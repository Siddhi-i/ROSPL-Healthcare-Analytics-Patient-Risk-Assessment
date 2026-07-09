# 🏥 Healthcare Analytics Dashboard

An interactive **Streamlit + Plotly** dashboard for analyzing patient healthcare data, with a bonus
**TextBlob** sentiment-analysis feature on patient clinical notes.

## ✨ Features

- **Patient Data Upload** — upload your own CSV/Excel file, or use the built-in sample dataset (500 synthetic patients)
- **Age Distribution** — histogram, age-group pie chart, summary statistics
- **Disease Distribution** — frequency bar chart, share-of-total pie chart, disease-by-gender breakdown
- **BMI Analysis** — distribution by category (Underweight/Normal/Overweight/Obese), BMI vs Age bubble chart
- **Blood Pressure Analysis** — systolic vs diastolic scatter plot, BP category classification, box plots
- **Gender Analysis** — gender split, age/BMI/BP comparisons by gender
- **KPI Cards** — total patients, average age, average BMI, average BP, % male, most common condition
- **Bonus: TextBlob Sentiment Analysis** — if your data has a `Notes` column, the dashboard automatically
  analyzes sentiment (Positive/Neutral/Negative) of clinical notes per disease
- **Sidebar Filters** — filter by age range, gender, and disease across the whole dashboard
- **Download filtered data** as CSV directly from the app

---

## 📁 Project Structure

```
healthcare_analytics_dashboard/
│
├── app.py                      # Main Streamlit dashboard application
├── generate_sample_data.py     # Script to (re)generate synthetic sample data
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── data/
    └── sample_patient_data.csv # Pre-generated sample dataset (500 patients)
```

---

## 🧰 Requirements

- **Python 3.13** (tested/compatible — you mentioned 3.13.14, which works fine)
- VS Code with the Python extension installed
- Internet connection (only needed once, to install packages)

---

## 🚀 Step-by-Step: Run in VS Code

### 1. Unzip and open the project
Unzip the downloaded folder, then in VS Code:
`File → Open Folder... → select healthcare_analytics_dashboard`

### 2. Open a terminal in VS Code
`Terminal → New Terminal` (make sure it's pointed at the project folder)

### 3. Create a virtual environment (recommended)
```bash
python -m venv venv
```

Activate it:
- **Windows (PowerShell):**
  ```bash
  venv\Scripts\Activate.ps1
  ```
- **Windows (cmd):**
  ```bash
  venv\Scripts\activate.bat
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

In VS Code, also select this environment as your interpreter:
`Ctrl+Shift+P → Python: Select Interpreter → choose the venv`

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. (Optional) Regenerate the sample dataset
A sample dataset is already included at `data/sample_patient_data.csv`. If you want a fresh
random sample, run:
```bash
python generate_sample_data.py
```

### 6. Run the dashboard
```bash
streamlit run app.py
```

### 7. View it in your browser
Streamlit will automatically open your default browser. If it doesn't, copy the URL shown
in the terminal, typically:

```
Local URL: http://localhost:8501
```

Paste that into your browser to view the dashboard.

### 8. Stop the app
Go back to the VS Code terminal and press `Ctrl + C`.

---

## 📤 Uploading Your Own Data

Use the **file uploader in the left sidebar** to upload a CSV or Excel file. Your file must
contain these columns (case-sensitive):

| Column        | Type    | Example       |
|---------------|---------|---------------|
| PatientID     | text    | P1001         |
| Age           | number  | 45            |
| Gender        | text    | Male / Female |
| BMI           | number  | 27.3          |
| Systolic_BP   | number  | 132           |
| Diastolic_BP  | number  | 84            |
| Disease       | text    | Hypertension  |
| Notes         | text (optional) | "Patient reports mild headache..." |

If the `Notes` column is present, the dashboard will automatically run TextBlob sentiment
analysis on it and display a sentiment breakdown under the **Disease Distribution** tab.

---

## 🛠️ Troubleshooting

- **`streamlit: command not found`** → make sure your virtual environment is activated and
  dependencies were installed (`pip install -r requirements.txt`).
- **Port already in use** → run `streamlit run app.py --server.port 8502` to use a different port.
- **Blank/error page after upload** → check that your file has all required columns listed above.
- **TextBlob errors on first run** → TextBlob's default pattern-based sentiment analyzer used in
  this project does not require downloading extra NLTK corpora, so no extra setup is needed.

---

## 📊 Tech Stack

- [Streamlit](https://streamlit.io/) — dashboard framework
- [Plotly Express](https://plotly.com/python/plotly-express/) — interactive charts
- [Pandas](https://pandas.pydata.org/) / [NumPy](https://numpy.org/) — data processing
- [TextBlob](https://textblob.readthedocs.io/) — sentiment analysis on patient notes

Enjoy exploring your healthcare data! 🎉

## Proof of Execution
<img width="1909" height="653" alt="Screenshot 2026-07-07 142701" src="https://github.com/user-attachments/assets/467851ae-bdaf-4061-aaa7-91c2815e9f93" />
<img width="369" height="901" alt="Screenshot 2026-07-07 142802" src="https://github.com/user-attachments/assets/311d3356-289f-4736-9d3d-291fb77e6385" />
<img width="1906" height="920" alt="Screenshot 2026-07-07 142719" src="https://github.com/user-attachments/assets/2ee6312a-e82d-445f-b726-ea8541d3edc7" />

