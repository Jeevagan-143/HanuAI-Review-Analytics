from pathlib import Path

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
DATA_DIR = BASE_DIR / "data"

st.set_page_config(
    page_title="HanuAI Review Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 HanuAI")
st.subheader("Intelligent Review Analytics & Predictive Insights Platform")
st.caption("Explore vehicle complaints, text patterns, and review sentiment.")

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Dashboard",
    ["Overview", "Vehicle Data Analysis", "Review Sentiment"]
)


def load_csv(path):
    if path.exists():
        try:
            return pd.read_csv(path)
        except Exception:
            return None
    return None


vehicle_data = load_csv(OUTPUT_DIR / "cleaned_vehicle_records.csv")
summary_data = load_csv(OUTPUT_DIR / "data_summary.csv")
frequent_terms = load_csv(OUTPUT_DIR / "frequent_terms.csv")
review_data = load_csv(DATA_DIR / "bestbuy_reviews.csv")


if page == "Overview":
    st.header("Project Overview")

    if vehicle_data is not None:
        total_records = len(vehicle_data)
        total_columns = len(vehicle_data.columns)
        missing_values = int(vehicle_data.isna().sum().sum())

        col1, col2, col3 = st.columns(3)
        col1.metric("Vehicle Records", f"{total_records:,}")
        col2.metric("Data Columns", total_columns)
        col3.metric("Missing Values", f"{missing_values:,}")

        st.markdown("### Vehicle Dataset Preview")
        st.dataframe(vehicle_data.head(10), use_container_width=True)
    else:
        st.warning(
            "Vehicle dataset not found. Check outputs/"
            "cleaned_vehicle_records.csv"
        )

    st.markdown("### Available Analysis")
    st.markdown(
        """
        - Vehicle complaint data exploration
        - Missing-value and dataset analysis
        - Frequent text term analysis
        - Customer review sentiment analysis
        """
    )

    if summary_data is not None:
        st.markdown("### Data Summary")
        st.dataframe(summary_data, use_container_width=True)


elif page == "Vehicle Data Analysis":
    st.header("🚗 Vehicle Data Analysis")

    if vehicle_data is not None:
        st.write("Explore the cleaned vehicle records.")

        search = st.text_input("Search records")

        filtered_data = vehicle_data.copy()

        if search:
            mask = filtered_data.astype(str).apply(
                lambda column: column.str.contains(
                    search, case=False, na=False
                )
            ).any(axis=1)
            filtered_data = filtered_data[mask]

        st.metric("Matching Records", len(filtered_data))
        st.dataframe(filtered_data, use_container_width=True)

        numeric_columns = filtered_data.select_dtypes(
            include="number"
        ).columns.tolist()

        if numeric_columns:
            selected_column = st.selectbox(
                "Choose a numeric column to visualize",
                numeric_columns
            )
            st.bar_chart(filtered_data[selected_column].value_counts().head(15))

    else:
        st.error("Cleaned vehicle dataset was not found.")

    if summary_data is not None:
        st.markdown("### Dataset Summary")
        st.dataframe(summary_data, use_container_width=True)

    if frequent_terms is not None:
        st.markdown("### Frequent Terms")
        st.dataframe(frequent_terms.head(30), use_container_width=True)

        numeric_columns = frequent_terms.select_dtypes(
            include="number"
        ).columns.tolist()

        if numeric_columns and len(frequent_terms.columns) > 1:
            text_columns = [
                column for column in frequent_terms.columns
                if column not in numeric_columns
            ]

            if text_columns:
                chart_data = frequent_terms.head(15).set_index(
                    text_columns[0]
                )[numeric_columns[0]]
                st.bar_chart(chart_data)


elif page == "Review Sentiment":
    st.header("💬 Customer Review Sentiment")

    if review_data is not None:
        st.info(
            "The current Best Buy review CSV contains synthetic demo "
            "reviews, not verified real customer reviews."
        )

        st.metric("Demo Reviews", len(review_data))
        st.dataframe(review_data, use_container_width=True)

        sentiment_columns = [
            column for column in review_data.columns
            if "sentiment" in column.lower()
        ]

        if sentiment_columns:
            sentiment_column = sentiment_columns[0]
            counts = review_data[sentiment_column].fillna(
                "Unknown"
            ).astype(str).value_counts()

            st.markdown("### Sentiment Distribution")
            st.bar_chart(counts)

            cols = st.columns(len(counts))
            for col, (sentiment, count) in zip(cols, counts.items()):
                col.metric(str(sentiment), int(count))

    else:
        st.warning(
            "Review dataset not found at data/bestbuy_reviews.csv"
        )

st.divider()
st.caption("HanuAI | Analytics dashboard")