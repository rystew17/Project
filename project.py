import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import altair as alt

estimated = pd.read_csv("https://raw.githubusercontent.com/rystew17/Project/main/Estimated%20Climate%20Data%20Included%20-%20Sheet1.csv")

raw = pd.read_csv("https://raw.githubusercontent.com/rystew17/Project/main/Raw%20Climate%20Data%20-%20Sheet1.csv")

countries = raw['Country\\year']

raw = raw.iloc[:,2:]
estimated = estimated.iloc[:,2:]

raw = raw.apply(pd.to_numeric, errors='coerce')
estimated = estimated.apply(pd.to_numeric, errors='coerce')

st.title('CSE 5544 Project')
st.data_frame(raw)
