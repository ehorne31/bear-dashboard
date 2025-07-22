import streamlit as st
import pandas as pd

st.set_page_config(page_title="My First App", layout="wide")
st.title("🐻 My First Bear Dashboard")
st.write("If you see this, your own app is running!")

df = pd.DataFrame({"BearID":[1,2,3],"Latitude":[28.4,28.6,28.7],"Longitude":[-81.2,-81.3,-81.1]})
st.dataframe(df)
