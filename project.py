import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import altair as alt

estimated = pd.read_csv("https://raw.githubusercontent.com/rystew17/Project/main/Estimated%20Climate%20Data%20Included%20-%20Sheet1%20(1).csv")

raw = pd.read_csv("https://raw.githubusercontent.com/rystew17/Project/main/Raw%20Climate%20Data%20-%20Sheet1.csv")


years = pd.DataFrame({'c1':['1990','1991','1992','1993','1994','1995','1996','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019']})

countries = raw['Country\year']
raw = raw.iloc[:,1:]
estimated = estimated.iloc[:,1:]
raw = raw.apply(pd.to_numeric, errors='coerce')
estimated = estimated.apply(pd.to_numeric, errors='coerce')



st.title('CSE 5544 Project')
option = st.select_slider("Select year", years)
type = st.radio("Include esitmated data? (Estimated Data is Highlighted Yellow)", ("Yes", "No"))
st.write("      Emissions by Country in " + option)
if type == "Yes":
    filter = estimated[option]
    filter2 = raw[option]
    data = pd.DataFrame({'c1':countries, 'c2':filter, 'c3':filter2})
    bar_chart = alt.Chart(data).mark_bar().encode(
        x = alt.X('c1',title = 'Country'),
        y = alt.Y('c2', title = 'Emissions'),
        color=alt.condition(
            alt.datum.c3 == 0,
            alt.value('yellow'),
            alt.value('green')
        )
    ).properties(
        width=750,
        height=500
    )
    st.altair_chart(bar_chart)
else:
    filter = raw[option]
    data = pd.DataFrame({'c1':countries, 'c2':filter})
    bar_chart = alt.Chart(data).mark_bar().encode(
        x = alt.X('c1',title='Countries'),
        y = alt.Y('c2',title='Emissions'),
        color=alt.condition(
            alt.datum.c2 >= 0,  # If the country is "US" this test returns True,
            alt.value('green'),     # highlight a bar with red.
            alt.value('lightgrey')   # And grey for the rest of the bars
        )
    ).properties(
        width=750,
        height=500
    )
    st.altair_chart(bar_chart)
    
  
    
