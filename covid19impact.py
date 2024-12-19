# Covid-19 Impacts Analysis (Case Study)
# The first wave of covid-19 impacted the global economy as the world was never ready for the pandemic. It resulted in a rise in cases, a rise in deaths, a rise in unemployment and a rise in poverty, resulting in an economic slowdown. Here, you are required to analyze the spread of Covid-19 cases and all the impacts of covid-19 on the economy.

# The dataset we are using to analyze the impacts of covid-19 is downloaded from Kaggle. It contains data about:

# the country code
# name of all the countries
# date of the record
# Human development index of all the countries
# Daily covid-19 cases
# Daily deaths due to covid-19
# stringency index of the countries
# the population of the countries
# GDP per capita of the countries

# import os
# print(os.getcwd())
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

data = pd.read_csv(r"C:\Users\Asus\OneDrive\Desktop\Final_year_Project\DA_projects\Covid-19\transformed_data.csv")
# data2 = pd.read_csv("raw_data.csv")
print(data)


# The data we are using contains the data on covid-19 cases and their impact on GDP from December 31, 2019, to October 10, 2020.

# Data Preparation
# The dataset that we are using here contains two data files. One file contains raw data, and the other file contains transformed one. But we have to use both datasets for this task, as both of them contain equally important information in different columns. So let’s have a look at both the datasets one by one:

# print(data.head())
# After having initial impressions of both datasets, I found that we have to combine both datasets by creating a new dataset. But before we create a new dataset, let’s have a look at how many samples of each country are present in the dataset:

print(data["COUNTRY"].value_counts())

# So we don’t have an equal number of samples of each country in the dataset. Let’s have a look at the mode value:

data["COUNTRY"].value_counts().mode()

# So 294 is the mode value. We will need to use it for dividing the sum of all the samples related to the human development index, GDP per capita, and the population. Now let’s create a new dataset by combining the necessary columns from both the datasets:



code = data["CODE"].unique().tolist()
country = data["COUNTRY"].unique().tolist()
hdi = []
tc = []
td = []
sti = []
population = data["POP"].unique().tolist()
gdp = []

for i in country:
    hdi.append((data.loc[data["COUNTRY"] == i, "HDI"]).sum()/294)
    tc.append((data.loc[data["COUNTRY"] == i, "TC"]).sum())
    td.append((data.loc[data["COUNTRY"] == i, "TD"]).sum())
    sti.append((data.loc[data["COUNTRY"] == i, "STI"]).sum()/294)
    population.append((data.loc[data["COUNTRY"] == i, "POP"]).sum()/294)

aggregated_data = pd.DataFrame(list(zip(code, country, hdi, tc, td, sti, population)), 
                               columns = ["Country Code", "Country", "HDI", 
                                          "Total Cases", "Total Deaths", 
                                          "Stringency Index", "Population"])
print(aggregated_data.head())


# import os
# print(os.getcwd())

# I have not included the GDP per capita column yet. I didn’t find the correct figures for GDP per capita in the dataset. So it will be better to manually collect the data about the GDP per capita of the countries.

# As we have so many countries in this data, it will not be easy to manually collect the data about the GDP per capita of all the countries. So let’s select a subsample from this dataset. To create a subsample from this dataset, I will be selecting the top 10 countries with the highest number of covid-19 cases. It will be a perfect sample to study the economic impacts of covid-19. So let’s sort the data according to the total cases of Covid-19:


# Sorting Data According to Total Cases

data = aggregated_data.sort_values(by=["Total Cases"], ascending=False)
print(data.head())

# Now here’s how we can select the top 10 countries with the highest number of cases:


# Top 10 Countries with Highest Covid Cases

data = data.head(10)
print(data)


# Now I will add two more columns (GDP per capita before Covid-19, GDP per capita during Covid-19) to this dataset:


data["GDP Before Covid"] = [65279.53, 8897.49, 2100.75, 
                            11497.65, 7027.61, 9946.03, 
                            29564.74, 6001.40, 6424.98, 42354.41]
data["GDP During Covid"] = [63543.58, 6796.84, 1900.71, 
                            10126.72, 6126.87, 8346.70, 
                            27057.16, 5090.72, 5332.77, 40284.64]
print(data)


# Analyzing the Spread of Covid-19
# Now let’s start by analyzing the spread of covid-19 in all the countries with the highest number of covid-19 cases. I will first have a look at all the countries with the highest number of covid-19 cases:



figure = px.bar(data, y='Total Cases', x='Country',
            title="Countries with Highest Covid Cases")
figure.show()



# We can see that the USA is comparatively having a very high number of covid-19 cases as compared to Brazil and India in the second and third positions. Now let’s have a look at the total number of deaths among the countries with the highest number of covid-19 cases:


figure = px.bar(data, y='Total Deaths', x='Country',
            title="Countries with Highest Deaths")
figure.show()


# Just like the total number of covid-19 cases, the USA is leading in the deaths, with Brazil and India in the second and third positions. One thing to notice here is that the death rate in India, Russia, and South Africa is comparatively low according to the total number of cases. Now let’s compare the total number of cases and total deaths in all these countries:


fig = go.Figure()
fig.add_trace(go.Bar(
    x=data["Country"],
    y=data["Total Cases"],
    name='Total Cases',
    marker_color='indianred'
))
fig.add_trace(go.Bar(
    x=data["Country"],
    y=data["Total Deaths"],
    name='Total Deaths',
    marker_color='lightsalmon'
))
fig.update_layout(barmode='group', xaxis_tickangle=-45)
fig.show()


# Now let’s have a look at the percentage of total deaths and total cases among all the countries with the highest number of covid-19 cases:


# Percentage of Total Cases and Deaths

cases = data["Total Cases"].sum()
deceased = data["Total Deaths"].sum()
labels = ["Total Cases", "Total Deaths"]
values = [cases, deceased]
fig = px.pie(data, values=values, names=labels, 
             title='Percentage of Total Cases and Deaths', hole=0.5)
fig.show()



# Below is how you can calculate the death rate of Covid-19 cases:


death_rate = (data["Total Deaths"].sum() / data["Total Cases"].sum()) * 100
print("Death Rate = ", death_rate)


# Another important column in this dataset is the stringency index. It is a composite measure of response indicators, including school closures, workplace closures, and travel bans. It shows how strictly countries are following these measures to control the spread of covid-19:

fig = px.bar(data, x='Country', y='Total Cases',
             hover_data=['Population', 'Total Deaths'], 
             color='Stringency Index', height=400, 
             title= "Stringency Index during Covid-19")
fig.show()


# Here we can see that India is performing well in the stringency index during the outbreak of covid-19


# Analyzing Covid-19 Impacts on Economy
# Now let’s move to analyze the impacts of covid-19 on the economy. Here the GDP per capita is the primary factor for analyzing the economic slowdowns caused due to the outbreak of covid-19. Let’s have a look at the GDP per capita before the outbreak of covid-19 among the countries with the highest number of covid-19 cases:


fig = px.bar(data, x='Country', y='Total Cases',
             hover_data=['Population', 'Total Deaths'], 
             color='GDP Before Covid', height=400, 
             title="GDP Per Capita Before Covid-19")
fig.show()


# Now let’s have a look at the GDP per capita during the rise in the cases of covid-19:


fig = px.bar(data, x='Country', y='Total Cases',
             hover_data=['Population', 'Total Deaths'], 
             color='GDP During Covid', height=400, 
             title="GDP Per Capita During Covid-19")
fig.show()


# Now let’s compare the GDP per capita before covid-19 and during covid-19 to have a look at the impact of covid-19 on the GDP per capita:



fig = go.Figure()
fig.add_trace(go.Bar(
    x=data["Country"],
    y=data["GDP Before Covid"],
    name='GDP Per Capita Before Covid-19',
    marker_color='indianred'
))
fig.add_trace(go.Bar(
    x=data["Country"],
    y=data["GDP During Covid"],
    name='GDP Per Capita During Covid-19',
    marker_color='lightsalmon'
))
fig.update_layout(barmode='group', xaxis_tickangle=-45)
fig.show()



# You can see a drop in GDP per capita in all the countries with the highest number of covid-19 cases.


# One other important economic factor is Human Development Index. It is a statistic composite index of life expectancy, education, and per capita indicators. Let’s have a look at how many countries were spending their budget on the human development:


fig = px.bar(data, x='Country', y='Total Cases',
             hover_data=['Population', 'Total Deaths'], 
             color='HDI', height=400, 
             title="Human Development Index during Covid-19")
fig.show()


# So this is how we can analyze the spread of Covid-19 and its impact on the economy.

# Conclusion
# In this task, we studied the spread of covid-19 among the countries and its impact on the global economy. We saw that the outbreak of covid-19 resulted in the highest number of covid-19 cases and deaths in the united states. One major reason behind this is the stringency index of the United States. It is comparatively low according to the population. We also analyzed how the GDP per capita of every country was affected during the outbreak of covid-19.


