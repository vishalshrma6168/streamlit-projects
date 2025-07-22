import streamlit as st

st.title("hello vishal")
st.subheader("hi")
st.write("Hello world")
st.text("welcome to our app")


# dropdown
chai=st.selectbox("your favorite chai",["hello","bye","etc"])
st.write(f"you choose :{chai}")

# alert box
st.success("your chai has been ready")

# wigets---element interaction ,button ,input etc

