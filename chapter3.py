import streamlit as st

# layout in streamlit
st.title("chai taste poll")

col1,col2=st.columns(2)
with col1:
  st.header("masala chai")
  vote1=st.button("vote masala chai")


with col2:
  st.header("adrak chai")
  st.image("img.jpg",width=300)
  vote2=st.button("vote adrak chai")


if vote1:
  st.success("thanks for voting masla chai")

elif vote2:
  st.success("thanks for voting adrak chai")


name=st.sidebar.text_input("enter your name")
# tea=st.slider.selectbox("choose your chai",["masala","kesar","adrak"])
st.write(f"welcome {name} ")

with st.expander("show chai making instructions"):
  st.write("""
1.boil water with tea leaves
2. add milk and spices
3.serve hot
""")
  

st.markdown("### welcome to chai app")

