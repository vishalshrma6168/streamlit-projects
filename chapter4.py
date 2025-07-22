# data se bat
import streamlit as st
import pandas as pd


st.title("chai sales dashboard")
file=st.file_uploader("uplod your csv file",type=["csv"])
if file:
 df= pd.read_csv(file)
 st.subheader("data preview")
 st.dataframe(df)


if file:
  st.subheader("summary stats")
  st.write(df.describe())


if file:
 cities= df["city"].unique()
 selectes_cities=st.selectbox("filter by cities",cities)
 filtereddata=df[df["city"] == selectes_cities]
 st.dataframe(filtereddata)