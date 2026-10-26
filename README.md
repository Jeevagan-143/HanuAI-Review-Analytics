\# HanuAI — Intelligent Review Analytics \& Predictive Insights Platform



\## Overview

HanuAI is a data analytics and text mining project focused on vehicle service and repair records. It explores recurring customer complaints, failure components, repair actions, and text patterns to support data-driven service insights.



\## Task 2: EDA \& Text Mining

\- Dataset inspection and duplicate removal

\- Missing-value analysis

\- Text cleaning and word-count analysis

\- TF-IDF-based term extraction

\- Exploratory K-Means text clustering

\- Category charts and Excel export

\- Markdown analysis report



\## Project Structure

\- `task2-eda-text-mining/` — Dataset and analysis script

\- `outputs/` — Cleaned data, summaries, Excel workbook, charts

\- `reports/` — EDA and text mining report

\- `requirements.txt` — Python dependencies



\## Run Locally

```bash

python -m venv .venv

```



Windows PowerShell:

```powershell

.\\.venv\\Scripts\\Activate.ps1

pip install -r requirements.txt

python .\\task2-eda-text-mining\\analyze\_data.py

```



\## Limitations

Text clusters are exploratory and do not establish confirmed root causes. Findings require domain validation.



\## Status

Task 2 analysis generated successfully. Task 1 review scraping and sentiment analysis remain to be completed.



