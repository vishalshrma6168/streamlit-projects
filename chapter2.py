
# streamlit run app.py
import streamlit as st

st.title("chai maker app")

if st.button("make chai"):
  st.success("your chai is ready")


# checkbox
add=st.checkbox("add masala")
if add:
  st.success("masala added to your chai")


# radio
tea_type=st.radio("pick your chai :",["milk","water","honey"])
st.success(tea_type)

# select box
flavour=st.selectbox("choose flavour",["adrak","patei"])
st.success(flavour)

# silder
sugar=st.slider("sugar level",0,5,8)
st.write(sugar)

# number input
st.number_input("how amany cups",min_value=1,max_value=10,step=1)

# ttext input
name=st.text_input("enter your name")
if name:
  st.write(name)


# dob
dob=st.date_input("select your date of birth")
st.write(dob)