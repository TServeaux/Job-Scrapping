# 🔍 Job Scraping Project

> Automated job offer aggregation from **France Travail** & **Adzuna** APIs — exported to CSV and ready for pandas analysis.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pandas](https://img.shields.io/badge/pandas-2.0+-150458?logo=pandas)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📖 Overview

Job Scraping Project is a Python application that aggregates job offers from multiple sources into a single, clean CSV file. It queries the **France Travail API** and the **Adzuna API**, merges the results, removes duplicates and exports the data for further analysis with pandas.

---

## 📁 Project Structure

```
Job-Scrapping/
├── Python/
│   ├── main.py            # Entry point — reads config and triggers the report
│   ├── requestsData.py    # API calls — authentication, France Travail, Adzuna
│   └── organize.py        # Data processing — formatting, CSV creation, dedup
├── data/
│   ├── user.json          # API credentials (client IDs and secrets)
│   └── data.json          # Search parameters (keyword, location, department)
└── output/                # Generated CSV files
```

---

## ⚙️ Installation

### Requirements

- Python 3.10+
- pip packages: `requests`, `pandas`

### Install dependencies

```bash
pip install requests pandas
```

---

## 🔧 Configuration

### `data/user.json`

Fill in your API credentials:

```json
{
  "franceTravail": {
    "userId": "YOUR_CLIENT_ID",
    "userAcces": "YOUR_CLIENT_SECRET"
  },
  "wtj": {
    "userId": "YOUR_ADZUNA_APP_ID",
    "userAcces": "YOUR_ADZUNA_APP_KEY"
  }
}
```

> Get your France Travail credentials at [francetravail.io](https://francetravail.io)  
> Get your Adzuna credentials at [developer.adzuna.com](https://developer.adzuna.com)

### `data/data.json`

Set your search parameters:

```json
{
  "keyWord": "python",
  "loc": "Lyon",
  "codeInsee": "69",
  "resN": 20
}
```

---

## 🚀 Usage

```bash
python main.py
```

The script will:

1. Fetch job offers from France Travail and Adzuna
2. Format and merge all results
3. Remove duplicates based on title, company and location
4. Save the output to `./output/{keyword}Jobs.csv`

---

## 🌐 Data Sources

| Source         | Type                          | Access                                          |
| -------------- | ----------------------------- | ----------------------------------------------- |
| France Travail | Official French job board API | Free — account required on francetravail.io     |
| Adzuna         | Job aggregator API            | Free — account required on developer.adzuna.com |

---

## 📄 Output

The generated CSV contains the following columns:

| Column        | Description                                 |
| ------------- | ------------------------------------------- |
| `source`      | France Travail or Adzuna                    |
| `titre`       | Job title                                   |
| `entreprise`  | Company name                                |
| `lieu`        | Location                                    |
| `contrat`     | Contract type (CDI, CDD, etc.)              |
| `salaire`     | Salary range if available                   |
| `date`        | Publication date                            |
| `lien`        | Link to the original offer                  |
| `description` | First 300 characters of the job description |

---

## 🛣️ Future Improvements

### ⏰ Automatic Daily Generation

Schedule the script to run automatically every day at a specific time:

**Windows — Task Scheduler**

> Configure a trigger at a fixed time (e.g. 08:00 AM) pointing to `python main.py`

**Linux / macOS — cron**

```bash
# Run every day at 8:00 AM
0 8 * * * python /path/to/main.py
```

**Cross-platform — `schedule` library**

```python
import schedule
import time

schedule.every().day.at("08:00").do(
    createReport, keyword, loc, codeInsee, resN
)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

### 🖥️ Graphical User Interface (GUI)

A desktop GUI built with **PyQt6** is planned to make the tool accessible to non-technical users.

Planned features:

- Search bar with keyword and department inputs
- Results table displaying all fetched offers
- Filters by contract type, source and date
- One-click CSV and Excel export
- Detail panel showing the full description on row click