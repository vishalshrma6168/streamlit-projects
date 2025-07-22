# api calls
import streamlit as st
import requests


st.title("live currency converter")
amount=st.number_input("enter the amount in INR",min_value=1)
target_currency=st.selectbox("cob=vert to:",["USD","EUR","GBP","JPY"])

if st.button("convert"):
  url="http://api.exchangerate-api.com/v4/latest/INR"