
from pathlib import Path
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "data" / "bestbuy_reviews.csv"
OUTPUT = ROOT / "outputs"

OUTPUT.mkdir(exist_ok=True)

df = pd.read_csv(INPUT)
df.columns = df.columns.str.strip().str.lower()

required = [
    "review_id", "product_title", "review_text",
    "review_date", "rating", "source", "reviewer"
]
missing = [col for col in required if col not in df.columns]
if missing:
    raise ValueError(f"CSV missing columns: {missing}")

df = df.drop_duplicates(subset=["review_id"])
df["review_date"] = pd.to_datetime(
    df["review_date"], errors="coerce"
).dt.strftime("%Y-%m-%d")

analyzer = SentimentIntensityAnalyzer()

def sentiment(text):
    score = analyzer.polarity_scores(str(text))["compound"]
    if score >= 0.05:
        label = "Positive"
    elif score <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"
    return pd.Series([label, score])

df[["sentiment", "sentiment_score"]] = df["review_text"].apply(sentiment)

def aspects(text):
    text = str(text).lower()
    tags = []
    keywords = {
        "Picture": ["picture", "screen", "color", "bright", "display"],
        "Sound": ["sound", "audio", "speaker"],
        "Setup": ["setup", "install", "easy to use"],
        "Smart Features": ["smart", "streaming", "remote", "features"],
        "Gaming": ["gaming", "game"],
        "Quality": ["quality", "problem", "problems", "stopped"]
    }
    for tag, words in keywords.items():
        if any(word in text for word in words):
            tags.append(tag)
    return ", ".join(tags) if tags else "General"

df["aspect_tags"] = df["review_text"].apply(aspects)

df.to_csv(OUTPUT / "bestbuy_reviews_sentiment.csv", index=False)

with pd.ExcelWriter(OUTPUT / "HanuAI_Task1_Review_Analysis.xlsx") as writer:
    df.to_excel(writer, sheet_name="Analyzed Reviews", index=False)
    df["sentiment"].value_counts().rename_axis(
        "Sentiment"
    ).reset_index(name="Count").to_excel(
        writer, sheet_name="Sentiment Summary", index=False
    )
    df["aspect_tags"].value_counts().rename_axis(
        "Aspect"
    ).reset_index(name="Count").to_excel(
        writer, sheet_name="Aspect Summary", index=False
    )

print("Task 1 analysis completed!")
print(f"Reviews analyzed: {len(df)}")
print("\nSentiment counts:")
print(df["sentiment"].value_counts())
print("\nOutput files:")
print(OUTPUT / "bestbuy_reviews_sentiment.csv")
print(OUTPUT / "HanuAI_Task1_Review_Analysis.xlsx")
print("\nNote: Verify whether these are genuine collected reviews before submission.")
