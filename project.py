import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import altair as alt

estimated = pd.read_csv("https://raw.githubusercontent.com/rystew17/Project/main/Estimated%20Climate%20Data%20Included%20-%20Sheet1.csv")

raw = pd.read_csv("https://raw.githubusercontent.com/rystew17/Project/main/Raw%20Climate%20Data%20-%20Sheet1.csv")


years = pd.DataFrame({'c1':[1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019]})

countries = raw['Country\year']
raw = raw.iloc[:,1:]
estimated = estimated.iloc[:,1:]
raw = raw.apply(pd.to_numeric, errors='coerce')
estimated = estimated.apply(pd.to_numeric, errors='coerce')


st.dataframe(raw)

st.title('CSE 5544 Project')

type = st.radio("Include esitmated data?", ("Yes", "No"))
if type == "Yes":
    option = st.selectbox("Select year", years)
    
else:
    st.write("you selected something else")
