import streamlit as st
import pandas as pd
import numpy as np

# ---- Title ----
st.set_page_config("📊 Student Analyzer", layout="centered")
st.title("📊 Student Performance Analyzer")

# ---- File Upload ----
uploaded_file = st.file_uploader("📂 Upload a CSV file", type=["csv"])

# ---- Grade Function ----
def get_grade(avg):
    if avg >= 90: return "A"
    elif avg >= 75: return "B"
    elif avg >= 60: return "C"
    elif avg >= 40: return "D"
    else: return "F"

# ---- Process Data ----
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if {"Name", "Maths", "Science", "English"}.issubset(df.columns):
        # Calculations
        df["Total"] = df[["Maths", "Science", "English"]].sum(axis=1)
        df["Average"] = np.round(df["Total"] / 3, 2)
        df["Grade"] = df["Average"].apply(get_grade)

        # Toppers
        top_score = df["Total"].max()
        toppers = df[df["Total"] == top_score]["Name"].tolist()

        # Subject-wise averages
        subject_avgs = df[["Maths", "Science", "English"]].mean()

        # ---- Display Results ----
        st.subheader("📋 Student Table")
        st.dataframe(df, use_container_width=True)

        st.subheader("🏆 Top Performer(s)")
        st.success(", ".join(toppers) + f" with {top_score} marks")

        st.subheader("📈 Subject Averages")
        for subject, avg in subject_avgs.items():
            st.write(f"**{subject}**: {avg:.2f}")
    else:
        st.error("CSV must include columns: Name, Maths, Science, English")
else:
    st.info("Upload a CSV file to begin analysis.")
