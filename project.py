import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import altair as alt

"hello cse 5544"

st.title("streamlit quick start")

st.header("Write and magic commands")

st.subheader("write subheader")

st.markdown("# h1")
st.markdown("## h2")
st.markdown("### h3")

st.latex("\sum_{0}^{n}i")

st.header("Display data")

st.subheader("Matplotlib chart")

df = pd.DataFrame({
    'c1':[1,2,3,4],
    'c2':[10,20,30,40]
})

data = pd.read_csv("https://raw.githubusercontent.com/CSE5544/data/main/ClimateData.csv")
data

#prepare the data
countries = data['Country\\year']
df_data_country = data.iloc[:,2:]
df_data_country = df_data_country.apply(pd.to_numeric, errors='coerce')
country_stats = pd.DataFrame({'country': countries, 'mean': df_data_country.mean(axis=1),
                       'std': df_data_country.std(axis=1)})

#render results
fig, ax = plt.subplots(figsize=(14, 6), dpi = 50)
ax.bar(countries, country_stats['mean'], yerr=country_stats['std'], capsize = 3)
ax.set_axisbelow(True)  #ensure the grid is under the graph elements
ax.margins(x=0.01) #set up the margin of graph
ax.grid(alpha = 0.3) #show the grid line
ax.set_xlabel('country')
ax.set_ylabel('emissions')
ax.set_title('The mean and std of emissions of countries')
xaxis = plt.xticks(rotation=90, ha='center', fontsize=8)
yaxis = plt.yticks(fontsize=8)

st.pyplot(fig)

st.subheader("altair chart")

chart_data = data.drop(columns=['Non-OECD Economies'])
chart_data = pd.melt(chart_data, id_vars=['Country\year'], var_name='year')
chart_data['value'] = chart_data['value'].apply(pd.to_numeric, errors='coerce')
chart_data.rename(columns={"Country\year": "country", "value":"emission"}, inplace = True)
chart_data

#render using altair
heatmap = alt.Chart(chart_data).mark_rect().encode(
    x=alt.X('country:N', title = 'country'),
    y=alt.Y('year:O', title = 'year'),
    color='emission:Q',
    tooltip=['country', 'year', 'emission']
)

st.altair_chart(heatmap, use_container_width = True)

st.header("widgets")

st.subheader("button")

st.button("click me")

if(st.button("about")):
    st.text("clicked about")

st.subheader("checkbox")

agree = st.checkbox("I agree")
if agree:
    st.write("Great, you agreed!")

st.subheader("radio")
type = st.radio("what's your favorite movie type?", ("Comedy", "Drama", "Action"))
if type == "Comedy":
    st.write("You selected Comedy")
else:
    st.write("you selected something else")

st.subheader("selectbox")
option = st.selectbox("country", ("USA", "China", "Europe Union"))

st.write(option)

st.subheader("multi-select")
option = st.multiselect("country", ("USA", "China", "Europe Union"), ("USA"))

st.write(option)

st.subheader("slider")
x = st.slider("x")
st.write("the square is", x * x)

st.header("Interactive chart")

st.subheader("interactive matplotlib chart")

options = st.multiselect("select countries", countries, ['Australia'])

country_stats.set_index("country", inplace=True)


fig, ax = plt.subplots(figsize=(14, 6), dpi = 50)
ax.bar(options, country_stats.loc[options]['mean'], yerr=country_stats.loc[options]['std'], capsize = 3)
ax.set_axisbelow(True)  #ensure the grid is under the graph elements
ax.margins(x=0.01) #set up the margin of graph
ax.grid(alpha = 0.3) #show the grid line
ax.set_xlabel('country')
ax.set_ylabel('emissions')
ax.set_title('The mean and std of emissions of countries')
xaxis = plt.xticks(rotation=90, ha='center', fontsize=8)
yaxis = plt.yticks(fontsize=8)

st.pyplot(fig)

st.subheader("interactive altair chart")

option = st.selectbox("select one country", countries)

filter_data = chart_data[chart_data['country'] == option]
bar_chart = alt.Chart(filter_data).mark_bar().encode(
    x = 'year:O',
    y = 'emission:Q'
)

st.altair_chart(bar_chart, use_container_width = True)
