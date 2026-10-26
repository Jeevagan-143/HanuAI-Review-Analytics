
import ast
import re
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "task2-eda-text-mining" / "Hanuai_task2_assignment.csv"
OUT = ROOT / "outputs"
REPORTS = ROOT / "reports"

OUT.mkdir(exist_ok=True)
REPORTS.mkdir(exist_ok=True)

df = pd.read_csv(DATA, low_memory=False)
df.columns = [str(c).strip() for c in df.columns]

print("Dataset shape:", df.shape)
print("Columns:", df.columns.tolist())

# Clean column names and values
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].astype("string").str.strip()

df = df.drop_duplicates().copy()

# Find date columns and parse dates
for col in df.columns:
    if "date" in col.lower() or "time" in col.lower():
        df[col] = pd.to_datetime(
    df[col], errors="coerce", utc=True
).dt.tz_localize(None)

# Detect free-text columns by their names
text_candidates = [
    c for c in df.columns
    if any(k in c.lower() for k in [
        "verbatim", "description", "comment", "text", "cause",
        "correction", "concern", "issue", "customer"
    ])
]

# Combine free-text fields for analysis
if text_candidates:
    df["combined_text"] = (
        df[text_candidates].fillna("").astype(str).agg(" ".join, axis=1)
    )
else:
    df["combined_text"] = ""

def clean_text(value):
    value = str(value).lower()
    value = re.sub(r"http\S+|www\.\S+", " ", value)
    value = re.sub(r"[^a-z0-9\s]", " ", value)
    return re.sub(r"\s+", " ", value).strip()

df["clean_text"] = df["combined_text"].map(clean_text)
df["text_length"] = df["clean_text"].str.len()
df["word_count"] = df["clean_text"].str.split().str.len()

# Extract frequent terms
terms = []
texts = df["clean_text"].fillna("")
if texts.str.strip().ne("").any():
    vectorizer = TfidfVectorizer(
        stop_words="english", max_features=100,
        ngram_range=(1, 2), min_df=1
    )
    matrix = vectorizer.fit_transform(texts)
    terms = sorted(
        zip(vectorizer.get_feature_names_out(),
            matrix.mean(axis=0).A1),
        key=lambda item: item[1],
        reverse=True
    )
    pd.DataFrame(terms, columns=["term", "mean_tfidf"]).to_csv(
        OUT / "frequent_terms.csv", index=False
    )

    # Group records into exploratory text clusters
    if len(df) >= 3:
        cluster_count = min(5, len(df) - 1)
        model = KMeans(n_clusters=cluster_count, random_state=42, n_init=10)
        df["text_cluster"] = model.fit_predict(matrix)
    else:
        df["text_cluster"] = 0
else:
    df["text_cluster"] = -1

# Missing-value and numeric summaries
missing = df.isna().sum().rename("missing_count").to_frame()
missing["missing_percent"] = (missing["missing_count"] / max(len(df), 1) * 100).round(2)
missing.to_csv(OUT / "missing_values.csv")

df.describe(include="all").transpose().to_csv(OUT / "data_summary.csv")
df.to_csv(OUT / "cleaned_vehicle_records.csv", index=False)

# Export Excel workbook
with pd.ExcelWriter(OUT / "HanuAI_Task2_Analysis.xlsx", engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Cleaned Data", index=False)
    missing.to_excel(writer, sheet_name="Missing Values")
    df.describe(include="all").transpose().to_excel(
        writer, sheet_name="Data Summary"
    )

# Generate charts
sns.set_theme()
for col in df.columns:
    if df[col].nunique(dropna=True) > 1 and df[col].nunique(dropna=True) <= 15:
        if df[col].dtype == "object" or isinstance(df[col].dtype, pd.CategoricalDtype):
            counts = df[col].value_counts().head(10)
            if not counts.empty:
                plt.figure(figsize=(10, 5))
                counts.plot(kind="bar")
                plt.title(f"Top categories: {col}")
                plt.xlabel(col)
                plt.ylabel("Record count")
                plt.tight_layout()
                safe = re.sub(r"[^a-zA-Z0-9_-]", "_", col)
                plt.savefig(OUT / f"category_{safe}.png", dpi=150)
                plt.close()

plt.figure(figsize=(9, 5))
df["word_count"].plot(kind="hist", bins=20)
plt.title("Distribution of Text Word Counts")
plt.xlabel("Word count")
plt.ylabel("Records")
plt.tight_layout()
plt.savefig(OUT / "text_word_count_distribution.png", dpi=150)
plt.close()

# Create a report using actual dataset values
report = [
    "# HanuAI — Task 2: EDA & Text Mining",
    "",
    "## Dataset overview",
    f"- Rows after duplicate removal: {len(df)}",
    f"- Columns: {len(df.columns)}",
    f"- Duplicate rows removed: {pd.read_csv(DATA, low_memory=False).duplicated().sum()}",
    f"- Text fields used: {', '.join(text_candidates) if text_candidates else 'No matching free-text columns detected'}",
    "",
    "## Data quality",
    f"- Columns with missing values: {(missing['missing_count'] > 0).sum()}",
    f"- Total missing cells: {int(missing['missing_count'].sum())}",
    "",
    "## Text analysis",
    f"- Average text word count: {df['word_count'].mean():.2f}",
    f"- Number of exploratory clusters: {df['text_cluster'].nunique()}",
    "",
    "## Frequent terms",
]
report.extend([f"- {term}: {score:.4f}" for term, score in terms[:20]])
report += [
    "",
    "## Business interpretation",
    "- Review the category charts to identify frequently reported components or issue types.",
    "- Review frequent terms and cluster examples to investigate recurring service concerns.",
    "- Treat clusters as exploratory groups, not confirmed root causes.",
    "- Validate suspected trends with domain experts before making operational decisions.",
    "",
    "## Outputs",
    "- cleaned_vehicle_records.csv",
    "- missing_values.csv",
    "- data_summary.csv",
    "- HanuAI_Task2_Analysis.xlsx",
    "- PNG charts",
]
(REPORTS / "Task2_EDA_TextMining_Report.md").write_text(
    "\n".join(report), encoding="utf-8"
)

print("\nSUCCESS! Task 2 analysis completed.")
print("Outputs:", OUT)
print("Report:", REPORTS / "Task2_EDA_TextMining_Report.md")
