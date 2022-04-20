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
st.text("       Emissions by Country in " + option)
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
    
    
    
    from google.colab import auth
auth.authenticate_user()
import gspread

#from oauth2client.client import GoogleCredentials  #remove this line
#gc = gspread.authorize(GoogleCredentials.get\_application\_default()) #remove this line

from google.auth import default
creds, _ = default()
gc = gspread.authorize(creds)

# access the google sheet and load it into pandas dataframe
#################### Do this only at the first time
wkbook = 'https://docs.google.com/spreadsheets/d/1HiVAuTr1miXHKCmxRDu_ZspUXttlRINN3ec2CvFHg1k/edit?usp=sharing'

wb = gc.open_by_url(wkbook)
sheet = wb.worksheet('Sheet1')
sheet_data = sheet.get_all_values()

df_data = pd.DataFrame(sheet_data)
# make row 0 into the column headers, then drop it
df_data.columns = df_data.iloc[0]
df_data.drop(df_data.index[0], inplace=True)

# Convert all year columns to float data type
cols = df_data.columns.drop(['Country\year', 'Non-OECD Economies'])
df_data[cols] = df_data[cols].apply(pd.to_numeric, errors = 'coerce')

# Drop Non-OECD Economies column
data = df_data.drop(columns=['Non-OECD Economies'])
data = pd.melt(data, id_vars=['Country\year'], var_name=['year'])
data['value'] = data['value'].apply(pd.to_numeric, errors='coerce')
data = data.rename(columns={'Country\year' : 'Country/Region'})

data.head(5)

# Initialize a grid of plots
grid = sns.FacetGrid(data, col="Country/Region", hue="Country/Region", palette="husl",
                     col_wrap=9, height=4, aspect=1.5)

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
    ax.text(x='1993', y=17000000, s="'92: UNFCCC", horizontalalignment='left', color="indianred")
    ax.text(x='2006', y=17000000, s="'05: Kyoto Protocol", horizontalalignment='left', color="indianred")
    ax.text(x='2016', y=16500000, s="'15: Paris \nAccord", horizontalalignment='left', color="indianred")

# Initialize the figure style
plt.style.use('seaborn-darkgrid')
 
# create a color palette
palette = plt.get_cmap('Set1')
 
# multiple line plot
num=0
for column in data.drop('year', axis=1):
    num+=1
 
    # Find the right spot on the plot
    plt.subplot(3,3, num)
 
    # plot every group, but discrete
    for v in data.drop('year', axis=1):
        plt.plot(data['year'], data[v], marker='', color='grey', linewidth=0.6, alpha=0.3)
 
    # Plot the lineplot
    plt.plot(data['year'], data[column], marker='', color=palette(num), linewidth=2.4, alpha=0.9, label=column)
 
    # Same limits for every chart
    plt.xlim(0,10)
    plt.ylim(-2,22)
 
    # Not ticks everywhere
    if num in range(7) :
        plt.tick_params(labelbottom='off')
    if num not in [1,4,7] :
        plt.tick_params(labelleft='off')
 
    # Add title
    plt.title(column, loc='left', fontsize=12, fontweight=0, color=palette(num) )

# general title
#plt.suptitle("How the 9 students improved\nthese past few days?", fontsize=13, fontweight=0, color='black', style='italic', y=1.02)
 
# Axis titles
#plt.text(0.5, 0.02, 'Time', ha='center', va='center')
#plt.text(0.06, 0.5, 'Note', ha='center', va='center', rotation='vertical')

# Show the graph
plt.show()

# Initialize the figure style
plt.style.use('seaborn-darkgrid')
 
# create a color palette
palette = plt.get_cmap('Set1')
 

# multiple line plot
num=0
for column in data.drop('year', axis=1):
    num+=1
 
    # Find the right spot on the plot
    plt.subplot(3,3, num)
 
    # plot every group, but discrete
    for v in data.drop('year', axis=1):
        plt.plot(data['year'], data[v], marker='', color='grey', linewidth=0.6, alpha=0.3)

data10 = data.sort_values(by=['value'])
data10 = data10[1:10] 
data10.headfrom google.colab import auth
auth.authenticate_user()
import gspread

#from oauth2client.client import GoogleCredentials  #remove this line
#gc = gspread.authorize(GoogleCredentials.get\_application\_default()) #remove this line

from google.auth import default
creds, _ = default()
gc = gspread.authorize(creds)

# access the google sheet and load it into pandas dataframe
#################### Do this only at the first time
wkbook = 'https://docs.google.com/spreadsheets/d/1HiVAuTr1miXHKCmxRDu_ZspUXttlRINN3ec2CvFHg1k/edit?usp=sharing'

wb = gc.open_by_url(wkbook)
sheet = wb.worksheet('Sheet1')
sheet_data = sheet.get_all_values()

df_data = pd.DataFrame(sheet_data)
# make row 0 into the column headers, then drop it
df_data.columns = df_data.iloc[0]
df_data.drop(df_data.index[0], inplace=True)

# Convert all year columns to float data type
cols = df_data.columns.drop(['Country\year', 'Non-OECD Economies'])
df_data[cols] = df_data[cols].apply(pd.to_numeric, errors = 'coerce')

# Drop Non-OECD Economies column
data = df_data.drop(columns=['Non-OECD Economies'])
data = pd.melt(data, id_vars=['Country\year'], var_name=['year'])
data['value'] = data['value'].apply(pd.to_numeric, errors='coerce')
data = data.rename(columns={'Country\year' : 'Country/Region'})

data.head(5)

# Initialize a grid of plots
grid = sns.FacetGrid(data, col="Country/Region", hue="Country/Region", palette="husl",
                     col_wrap=9, height=4, aspect=1.5)

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
    ax.text(x='1993', y=17000000, s="'92: UNFCCC", horizontalalignment='left', color="indianred")
    ax.text(x='2006', y=17000000, s="'05: Kyoto Protocol", horizontalalignment='left', color="indianred")
    ax.text(x='2016', y=16500000, s="'15: Paris \nAccord", horizontalalignment='left', color="indianred")

# Initialize the figure style
plt.style.use('seaborn-darkgrid')
 
# create a color palette
palette = plt.get_cmap('Set1')
 
# multiple line plot
num=0
for column in data.drop('year', axis=1):
    num+=1
 
    # Find the right spot on the plot
    plt.subplot(3,3, num)
 
    # plot every group, but discrete
    for v in data.drop('year', axis=1):
        plt.plot(data['year'], data[v], marker='', color='grey', linewidth=0.6, alpha=0.3)
 
    # Plot the lineplot
    plt.plot(data['year'], data[column], marker='', color=palette(num), linewidth=2.4, alpha=0.9, label=column)
 
    # Same limits for every chart
    plt.xlim(0,10)
    plt.ylim(-2,22)
 
    # Not ticks everywhere
    if num in range(7) :
        plt.tick_params(labelbottom='off')
    if num not in [1,4,7] :
        plt.tick_params(labelleft='off')
 
    # Add title
    plt.title(column, loc='left', fontsize=12, fontweight=0, color=palette(num) )

# general title
#plt.suptitle("How the 9 students improved\nthese past few days?", fontsize=13, fontweight=0, color='black', style='italic', y=1.02)
 
# Axis titles
#plt.text(0.5, 0.02, 'Time', ha='center', va='center')
#plt.text(0.06, 0.5, 'Note', ha='center', va='center', rotation='vertical')

# Show the graph
plt.show()

# Initialize the figure style
plt.style.use('seaborn-darkgrid')
 
# create a color palette
palette = plt.get_cmap('Set1')
 

# multiple line plot
num=0
for column in data.drop('year', axis=1):
    num+=1
 
    # Find the right spot on the plot
    plt.subplot(3,3, num)
 
    # plot every group, but discrete
    for v in data.drop('year', axis=1):
        plt.plot(data['year'], data[v], marker='', color='grey', linewidth=0.6, alpha=0.3)

data10 = data.sort_values(by=['value'])
data10 = data10[1:10] 
data10.head
    
  
    
