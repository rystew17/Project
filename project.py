import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import altair as alt

estimated = pd.read_csv("https://raw.githubusercontent.com/rystew17/Project/main/Estimated%20Climate%20Data%20Included%20-%20Sheet1%20(1).csv")

raw = pd.read_csv("https://raw.githubusercontent.com/rystew17/Project/main/Raw%20Climate%20Data%20-%20Sheet1%20(1).csv")

years = pd.DataFrame({'c1':['1990','1991','1992','1993','1994','1995','1996','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019']})

countries = raw['Country\year']
raw = raw.iloc[:,1:]
estimated = estimated.iloc[:,1:]
raw = raw.apply(pd.to_numeric, errors='coerce')
estimated = estimated.apply(pd.to_numeric, errors='coerce')



st.title('CSE 5544 Project')
option = st.select_slider("Select year", years)
type = st.radio("Include esitmated data? (Estimated Data is Highlighted Yellow)", ("Yes", "No"))
st.text("Emissions by Country in " + option)
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
    
df_data = pd.read_csv("https://raw.githubusercontent.com/rystew17/Project/main/CSE5544.Lab1.ClimateData%20-%20Sheet1.csv")

plt.style.use('seaborn')

#difference in average emission across years for non OECD vs OECD economies 
#comparison of emission before and after 2015 conference 
#comparison of emission between big five from UN


df_copy1 = df_data.set_index('Country\year')
df_copy1.drop( index='OECD - Total', inplace = True)
df_copy1.drop( index='OECD - Europe', inplace = True)
df_copy1.reset_index(inplace = True)
column_names = df_copy1.columns.values
years = list(column_names)
years.remove('Country\year')
years.remove('Non-OECD Economies')

non_oecd_econ = df_copy1[(df_copy1["Non-OECD Economies"].isin(["Yes"]))]
non_oecd_econ_calc = non_oecd_econ.iloc[:,2:]
non_oecd_econ_calc = non_oecd_econ_calc.apply(pd.to_numeric, errors='coerce')
oecd_econ = df_copy1[(df_copy1["Non-OECD Economies"].isin(["No"]))]
oecd_econ_calc = oecd_econ.iloc[:,2:]
oecd_econ_calc = oecd_econ_calc.apply(pd.to_numeric, errors='coerce')

all_countries = df_copy1['Country\year']
statisticsNon = pd.DataFrame({'TOTAL': non_oecd_econ_calc.sum(),'AVERAGE': non_oecd_econ_calc.mean(), 'STN. DEVIATION':non_oecd_econ_calc.std()})
statistics = pd.DataFrame({'TOTAL': oecd_econ_calc.sum(),'AVERAGE': oecd_econ_calc.mean(), 'STN. DEVIATION':oecd_econ_calc.std()})

five_years_copy = non_oecd_econ[["Country\year","Non-OECD Economies", "2005","2010","2012","2014","2016"]]
five_years = five_years_copy[["Country\year", "2005","2010","2012","2014","2016"]]

five_years['2005']= five_years['2005'].apply(pd.to_numeric, errors = 'coerce')
five_years['2010']= five_years['2010'].apply(pd.to_numeric, errors = 'coerce')
five_years['2012']= five_years['2012'].apply(pd.to_numeric, errors = 'coerce')
five_years['2014']= five_years['2014'].apply(pd.to_numeric, errors = 'coerce')
five_years['2016']= five_years['2016'].apply(pd.to_numeric, errors = 'coerce')
five_years['2005percent'] = (five_years['2005'] / five_years['2005'].sum())*100
five_years['2010percent'] = (five_years['2010'] / five_years['2010'].sum())*100
five_years['2012percent'] = (five_years['2012'] / five_years['2012'].sum())*100
five_years['2014percent'] = (five_years['2014'] / five_years['2014'].sum())*100
five_years['2016percent'] = (five_years['2016'] / five_years['2016'].sum())*100
five_years_percent = five_years[["Country\year","2005percent","2010percent","2012percent","2014percent","2016percent"]]

sorted1 = five_years_percent.sort_values(by=['2005percent'], ascending = False)
sorted1 = sorted1.head(5)[["Country\year","2005percent"]]
sorted2 = five_years_percent.sort_values(by=['2010percent'], ascending = False)
sorted2 = sorted2.head(5)[["Country\year","2010percent"]]
sorted3 = five_years_percent.sort_values(by=['2012percent'], ascending = False)
sorted3 = sorted3.head(5)[["Country\year","2012percent"]]
sorted4 = five_years_percent.sort_values(by=['2014percent'], ascending = False)
sorted4 = sorted4.head(5)[["Country\year","2014percent"]]
sorted5 = five_years_percent.sort_values(by=['2016percent'], ascending = False)
sorted5 = sorted5.head(5)[["Country\year","2016percent"]]

continents = ['North America', 'South America','Asia', 'Europe']
northAmerica = ['OECD America']
southAmerica = ['Brazil']
Asia = ['China (People\'s Republic of)', 'Indonesia','India']
Europe = ['Russia']

value1 = sorted1[(sorted1["Country\\year"].isin(northAmerica))]
value2 = sorted1[(sorted1["Country\\year"].isin(southAmerica))]
value3 = sorted1[(sorted1["Country\\year"].isin(Asia))]
value4 = sorted1[(sorted1["Country\\year"].isin(Europe))]

statisticsAsiaY1 = pd.DataFrame({'TOTAL': value3.sum()})
statisticsEuropeY1 = pd.DataFrame({'TOTAL': value4.sum()})
statisticsSAY1 = pd.DataFrame({'TOTAL': value2.sum()})
statisticsNAY1 = pd.DataFrame({'TOTAL': value1.sum()})

value12 = sorted2[(sorted2["Country\\year"].isin(northAmerica))]
value22 = sorted2[(sorted2["Country\\year"].isin(southAmerica))]
value32 = sorted2[(sorted2["Country\\year"].isin(Asia))]
value42 = sorted2[(sorted2["Country\\year"].isin(Europe))]

statisticsAsiaY2 = pd.DataFrame({'TOTAL': value32.sum()})
statisticsEuropeY2 = pd.DataFrame({'TOTAL': value42.sum()})
statisticsSAY2 = pd.DataFrame({'TOTAL': value22.sum()})
statisticsNAY2 = pd.DataFrame({'TOTAL': value12.sum()})

value13 = sorted3[(sorted3["Country\\year"].isin(northAmerica))]
value23 = sorted3[(sorted3["Country\\year"].isin(southAmerica))]
value33 = sorted3[(sorted3["Country\\year"].isin(Asia))]
value43 = sorted3[(sorted3["Country\\year"].isin(Europe))]

statisticsAsiaY3 = pd.DataFrame({'TOTAL': value33.sum()})
statisticsEuropeY3 = pd.DataFrame({'TOTAL': value43.sum()})
statisticsSAY3 = pd.DataFrame({'TOTAL': value23.sum()})
statisticsNAY3 = pd.DataFrame({'TOTAL': value13.sum()})

value14 = sorted4[(sorted4["Country\\year"].isin(northAmerica))]
value24 = sorted4[(sorted4["Country\\year"].isin(southAmerica))]
value34 = sorted4[(sorted4["Country\\year"].isin(Asia))]
value44 = sorted4[(sorted4["Country\\year"].isin(Europe))]

statisticsAsiaY4 = pd.DataFrame({'TOTAL': value34.sum()})
statisticsEuropeY4 = pd.DataFrame({'TOTAL': value44.sum()})
statisticsSAY4 = pd.DataFrame({'TOTAL': value24.sum()})
statisticsNAY4 = pd.DataFrame({'TOTAL': value14.sum()})

value15 = sorted5[(sorted5["Country\\year"].isin(northAmerica))]
value25 = sorted5[(sorted5["Country\\year"].isin(southAmerica))]
value35 = sorted5[(sorted5["Country\\year"].isin(Asia))]
value45 = sorted5[(sorted5["Country\\year"].isin(Europe))]

statisticsAsiaY5 = pd.DataFrame({'TOTAL': value35.sum()})
statisticsEuropeY5 = pd.DataFrame({'TOTAL': value45.sum()})
statisticsSAY5 = pd.DataFrame({'TOTAL': value25.sum()})
statisticsNAY5 = pd.DataFrame({'TOTAL': value15.sum()})

ContinentsYear1 = [statisticsNAY1.iloc[1,0], statisticsSAY1.iloc[1,0], statisticsAsiaY1.iloc[1,0], statisticsEuropeY1.iloc[1,0] ]
ContinentsYear2 = [statisticsNAY2.iloc[1,0], statisticsSAY2.iloc[1,0], statisticsAsiaY2.iloc[1,0], statisticsEuropeY2.iloc[1,0] ]
ContinentsYear3 = [statisticsNAY3.iloc[1,0], statisticsSAY3.iloc[1,0], statisticsAsiaY3.iloc[1,0], statisticsEuropeY3.iloc[1,0] ]
ContinentsYear4 = [statisticsNAY4.iloc[1,0], statisticsSAY4.iloc[1,0], statisticsAsiaY4.iloc[1,0], statisticsEuropeY4.iloc[1,0] ]
ContinentsYear5 = [statisticsNAY5.iloc[1,0], statisticsSAY5.iloc[1,0], statisticsAsiaY5.iloc[1,0], statisticsEuropeY5.iloc[1,0] ]

plt.rcParams["figure.figsize"] = [20, 16]
plt.rcParams["figure.autolayout"] = True

fig, ax = plt.subplots()
size = 0.3
colorsForChart = ['#849AE4','#A60A06','#93B581','#652D35'];
ax.pie(ContinentsYear1, pctdistance=0.9,autopct ='%1.1f%%', colors=colorsForChart,labels=continents,labeldistance = 1, radius=2.2,wedgeprops=dict(width=1.5*size,edgecolor='w'))
ax.pie(ContinentsYear2, pctdistance=0.85, autopct ='%1.1f%%', colors=colorsForChart, labels=continents,labeldistance = 0.91, radius=2.2-1.5*size, wedgeprops=dict(width=1.5*size, edgecolor='w'))
ax.pie(ContinentsYear3, pctdistance=0.8, autopct ='%1.1f%%',colors=colorsForChart, labels=continents,labeldistance = 0.87,radius=2.2-3*size, wedgeprops=dict(width=1.5*size, edgecolor='w'))
ax.pie(ContinentsYear4, pctdistance=0.72, autopct ='%1.1f%%',colors=colorsForChart, labels=continents,labeldistance = 0.82,radius=2.2-4.5*size, wedgeprops=dict(width=1.5*size, edgecolor='w'))
ax.pie(ContinentsYear5, pctdistance=0.64, autopct ='%1.1f%%',colors=colorsForChart, labels=continents,labeldistance = 0.78,radius=2.2-6*size, wedgeprops=dict(width=1.5*size, edgecolor='w'))
plt.show()
st.text("Contributions based on Continents of top 5 emittors during 5 largest emission years ")
st.pyplot(fig)

data = pd.read_csv("https://raw.githubusercontent.com/rystew17/Project/main/LineChart%20Data%20-%20Sheet1.csv")
data = pd.melt(data, id_vars=['Country\year'], var_name=['year'])
data['value'] = data['value'].apply(pd.to_numeric, errors='coerce')
data = data.rename(columns={'Country\year' : 'Country/Region'})

data.head(5)

# Initialize a grid of plots
grid = sns.FacetGrid(data, col="Country/Region", hue="Country/Region", palette="husl",
                     col_wrap=2, height=8, aspect=1.5)

# Draw a horizontal line to show the starting point
grid.refline(y=0, linestyle=":")

# Draw a line plot to show emissions values
grid.map(plt.plot, "year", "value", marker="o")

grid.set_xticklabels(rotation=90)
grid.set_ylabels('Greenhouse Gas Emissions \n(millions of tons of CO2)')

# Adjust the arrangement of the plots
grid.fig.tight_layout(w_pad=1)

grid.refline(x = '1992', color="rosybrown", lw = 2)
grid.refline(x = '2005', color="rosybrown", lw = 2)
grid.refline(x = '2015', color="rosybrown", lw = 2)

for ax in grid.axes:
    ax.text(x='1993', y=15000000, s="'92: UNFCCC", horizontalalignment='left', color="indianred")
    ax.text(x='2006', y=15000000, s="'05: Kyoto Protocol", horizontalalignment='left', color="indianred")
    ax.text(x='2016', y=15000000, s="'15: Paris \nAccord", horizontalalignment='left', color="indianred")
st.pyplot(grid)
