'''Generally, this file unites cells of Jupyter notebook
into a streamlit page by its layout methods'''

import streamlit as st

# LIBRARIES
import math
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Sidebar
with st.sidebar:
    st.markdown(
        """# _Production by Maksim Kuptsov,\
        group 231-1_"""
    )
    st.divider()
    st.markdown("## _HSE DSBA Educational Data Science Project_")


# INTRODUCTION
st.title("Mercedes Used Car Listing")
data = pd.read_csv("data/merc.csv")

st.markdown("Current dataset provides information on characteristics of Mercedes-Benz cars on sale. Analyzing this dataset can be useful for people selling their car of this brand or for those who want to buy one.")


# DATA CLEANUP AND TRANSFORMATION + STRUCTURE
st.markdown("## Data structure, cleanup and transformation")
st.markdown("After importing all required libraries, I looked at the basic structure of the dataset and conducted data cleanup, namely made sure of datatypes, removed NaN fields, reduced all inconsistent values and got rid of \"Class\" postfix in 'model' What is more I added a new field: 'mpy'.")

# Whole data cleanup
initial_data = data
data.drop(12072, inplace=True)
data = data[data['mpg'] != 1.1]
data = data[data['engineSize'] != 0]
data = data[data['transmission'] != "Other"]
data = data[data['fuelType'] != "Other"]
for i, value in enumerate(data['model']):
    data.iloc[i, 0] = value.upper().replace("CLASS", "").strip()
data = data[(data['model'] != '180') & (data['model'] != '200') & (data['model'] != '220')]
mpy = (
    data['mileage'] / (2023 - data['year'])
).apply(math.ceil)
data.insert(5, 'mpy', mpy)

# Buttons
dbut = st.button("The initial dataset", key='d')
cbut = st.button("The clean and transformed dataset", key='c')
if dbut:
    st.markdown(f"_Shape: {initial_data.shape[0]} rows, {initial_data.shape[1]} columns_")
    st.dataframe(initial_data)
if cbut:
    st.markdown(f"_Shape: {data.shape[0]} rows, {data.shape[1]} columns_")
    st.dataframe(data)

st.markdown(
    f"""The latter consists of {data.shape[0]} items, which have {data.shape[1]} columns, namely
- model

    Model of the car in Mercedes product line.
- year

    Year of car's registration.
- price

    Price in euros.
- transmission

    Type of gear box.
- mileage

    Total distance used in miles.
- mpy
            
    Shows how intesively the car was used in the period between the year of its registration and 2023. In other words, **miles per year**.

- fuelType

    Fuel engine works on.
- tax

    Road tax — a tax which has to be paid on, or included with, a motorised vehicle to use it on a public road.
- mpg

    Miles per galoon. The characteristic shows how many miles can vehicle cover on 1 galoon of fuel.
    1 mile ~ 1.6 kilometres; 1 galoon ~ 3.79 litres.
- engineSize

    Size of engine in litres."""
)


# DESCRIPTIVE STATISTICS
st.markdown("## Descriptive Statistics")

st.markdown("Here I would like to briefly describe fields 'year', 'price', 'mileage', 'mpy', 'tax', 'mpg', 'engineSize' by showing their mean, median, standard deviation, minimum and maximum.")

descriptives = pd.DataFrame( {
    "mean": [
        data.iloc[:, i].mean() for i in range(1, data.shape[1]) if data.iloc[:, i].dtype in ('int64', 'float64')
    ],
    "median": [
        data.iloc[:, i].median() for i in range(1, data.shape[1]) if data.iloc[:, i].dtype in ('int64', 'float64')
    ],
    "standard deviation": [
        data.iloc[:, i].std() for i in range(1, data.shape[1]) if data.iloc[:, i].dtype in ('int64', 'float64')
    ],
    "minimum": [
        data.iloc[:, i].min() for i in range(1, data.shape[1]) if data.iloc[:, i].dtype in ('int64', 'float64')
    ],
    "maximum": [
        data.iloc[:, i].max() for i in range(1, data.shape[1]) if data.iloc[:, i].dtype in ('int64', 'float64')
    ]
},
index=['year', 'price', 'mileage', 'mpy', 'tax', 'mpg', 'engineSize']
)

st.dataframe(descriptives)


# OVERVIEW
st.markdown("## Overview")
st.markdown(
    """For the first glance at the data I have chosen fields 'year', 'price', 'mileage', 'engineSize' to gain understanding of how much people sell Mercedes cars for, of what age, mileage and engine size mostly.

Let me plot these characteristics to the items of the dataset and analyze the result."""
)

sns.set_style("whitegrid")

plt.rcParams["figure.figsize"] = (12,10)
plt.subplot(2, 2, (1, 2))
plt.title("Prices of cars presented in the dataset")
plt.xlabel("item_index")
plt.ylabel("price")
plt.scatter(data.index, data['price'], s=3)
plt.subplot(223)
plt.hist(data['mileage'], color='Darkgreen')
plt.title("Number of cars by mileage")
plt.xlabel("mileage")
plt.ylabel("quantity")
plt.subplot(224)
plt.hist(data['engineSize'], color='Darkblue')
plt.title("Number of cars by engine size")
plt.xlabel("engine size")
plt.ylabel("quantity")

# retrieve the Figure from the global state
st.pyplot(plt.gcf())
# Close current figure window so to display other plots
# Not plt.clf(), as for some reason the size of a canvas does not change
plt.close()

st.markdown(
    """As I can see, people tend to sell Mercedeses of mileage from 0 to 25000 and of engine size 2.0 considerably more often then others. Cars with engines of medium power are more than twice more popular on Mercedes resale market than compact ones. Hence, I can assume people choose other brands for more economic cars.

Also what stands out is that the majority asks from 10000 to 40000 euros for their car, that is most of the cars lie in price range between 10 and 40 thousand euros. It can be considered average price range."""
)

st.markdown("As for the 'year', I would like to look at relative quantity of cars on sale:")

plt.rcParams["figure.figsize"] = (9,4)
plt.ylabel("year")
plt.title("Volume of car sales by years")
plt.violinplot(data['year'], points=300)

st.pyplot(plt.gcf())
plt.close()

st.markdown(
    """It can be seen that people sell cars of 2019 year of registration mostly. There are several reasons for this. If we assume 2020 is the year of the data collection, then the following reasons ought to take place:

- Some people regularly update their auto. 2020 was the year of restyling, so a lot of people sold their "old" cars in order to buy the newest model. It is a common phenomenon among Mercedes-Benz clients. So, the wave of sales fell on the previous year, namely 2019.

- People buy a car, drive it for a short period of time (a year or less), disapprove of it and sell.

- Difficult financial situation. People take a car loan, but then realize they cannot cope with it.

There are also quite high volumes for 2017 and 2016. Overall, the quantity decreases as the year goes down, and becomes insignificant at 2010: obviously, the younger the model, the higher demand it is in."""
)


# DETAILED OVERVIEW
st.markdown("## Detailed Overview")
st.markdown("It is time to look at specifics of our data in order to find any reasonable patterns.")
st.markdown(
    """At first I want to analyse the relationship between each pair of numeric variables of the dataset by identifying respective correlations and plotting the most catchy dependencies.

I will use scatter plots mostly, because they are more universal and help to informatively present almost all types of pairwise data."""
)

sns.heatmap(
    data.loc[:, ['year', 'price', 'mileage', 'mpy', 'tax', 'mpg', 'engineSize']].corr(),
    annot = True,
    linewidth=0.5,
    square=True,
    cmap='coolwarm',
    center=0
)
st.pyplot(plt.gcf())
plt.close()

st.markdown("Consider positive correlations:")

years = range(data['year'].min(), data['year'].max() + 1)
mean_prices = pd.Series(
    (data[data['year'] == x]['price'].mean() for x in years),
    index=years
)

plt.rcParams["figure.figsize"] = (12,10)
plt.subplot(321)
plt.xlabel("mileage")
plt.ylabel("mpy")
plt.scatter(data['mileage'], data['mpy'], s=2, c='#C12B30')
plt.subplot(322)
plt.xlabel("year")
plt.ylabel("mean price")
plt.plot(mean_prices, c='#F39577')
plt.subplot(323)
plt.xlabel("engineSize")
plt.ylabel("price")
plt.scatter(data['engineSize'], data['price'], s=3, c='#F39577')
plt.subplot(324)
plt.xlabel("engineSize")
plt.ylabel("tax")
plt.scatter(data['engineSize'], data['tax'], s=5, c='#F7B79B')
plt.subplot(325)
plt.xlabel("mpg")
plt.ylabel("mpy")
plt.scatter(data['mpg'], data['mpy'], s=1, c='#F5C0A7')
plt.subplot(326)
plt.xlabel("tax")
plt.ylabel("price")
plt.scatter(data['tax'], data['price'], s=2, c='#F5C1A9')

st.pyplot(plt.gcf())
plt.close()

st.markdown(
    """- **'mpy'** against **'mileage'** (correlation **0.92**):

    Such correlation may seem obvious. If a car is used on a daily basis (regularly, in other words), then the more it was driven in general, the more it was driven yearly. The fact that the age of a car increases over time keeps this growth almost linear.
- **'year'** against **'price'** (correlation **0.53**, mean price on graph):

    The latest models cost more than their "ancestors" (cars of the same model, released earlier). This is due to marketing reasons mostly, newer cars are most desired and are considered more trustworthy.
- **'engineSize'** against **'price'** (correlation **0.52**):

    High correlation, indicating that engine size directly influences the price. It may not be noticed straightaway, since the car's age also contributes a lot to the price, as I have just showed.
- **'engineSize'** against **'tax'** (correlation **0.34**):

    Medium correlation shows that in general people pay higher road taxes for more powerful cars.
-  **'mpy'** against **'mpg'** (correlation **0.28**):

    Medium correlation, which I interpret as economical cars are used by people more regularly and intensively, rather than powerful and fuel-consuming. This could also be clearly observed in the plot.
- **'tax'** against **'price'** (correlation **0.27**):
 
    Medium correlation, not distinctively seen in a plot, shows that higher road taxes are set for more expensive cars. This may seem logical if we recall that higher engine size, accounting for the considerable part of the price, leads to higher tax."""
)

st.markdown("Consider negative correlations:")

mean_mileages = pd.Series(
    (data[data['year'] == x]['mileage'].mean() for x in years)
)

plt.rcParams["figure.figsize"] = (12,10)
plt.subplot(321)
plt.xlabel("year")
plt.ylabel("mean mileage")
plt.stem(years, mean_mileages)
plt.subplot(322)
plt.xlabel("mileage")
plt.ylabel("price")
plt.scatter(data['mileage'], data['price'], s=0.3, c='#86A9FC')
plt.subplot(323)
plt.xlabel("year")
plt.ylabel("mpy")
plt.scatter(data['year'], data['mpy'], s=2, c='#89ACFD')
plt.subplot(324)
plt.xlabel("mpy")
plt.ylabel("price")
plt.scatter(data['mpy'], data['price'], s=0.3, c='#8DB0FE')
plt.subplot(325)
plt.xlabel("tax")
plt.ylabel("mpg")
plt.scatter(data['tax'], data['mpg'], s=2, c='#89ACFD')
plt.subplot(326)
plt.xlabel("price")
plt.ylabel("mpg")
plt.scatter(data['price'], data['mpg'], s=0.3, c='#97B8FF')

st.pyplot(plt.gcf())
plt.close()

st.markdown(
    """- **'year'** against **'mileage'** (correlation **-0.75**, mean mileage on graph):

    Strong negative correlation implies that newer cars are of less mileage, which is expected.
- **'price'** against **'mileage'** (correlation **-0.54**):

    It can be observed that the higher mileage a car has, the cheaper it is.
- **'mpy'** against **'year'** (correlation **-0.52**):

    High correlation. What stands out is that cars of years 2015-2017 have the widest ranges of 'mpy'. I suppose it can be explained in the following way: cars of these years were (by 2020) of a certain age to gain high mileage (unlike newer ones), but not too old to allow its age to decrease 'mpy' while it is driven rarely (which happens to older cars).
- **'price'** against **'mpy'** (correlation **-0.5**):

    The situation is quite similar to 'price' ag. 'mileage': the more intensively the car was used, the cheaper it is.
- **'mpg'** against **'tax'** (correlation **-0.52**):

    High correlation illustrates that higher fuel consumption results in higher tax.
- **'mpg'** against **'price'** (correlation **-0.44**):

    Medium negative correlation indicates that on average the lesser the 'mpy', the more the car costs. Low values of 'mpy' are associated with powerful expensive engines."""
)

st.markdown(
    """I also want to consider the dataset with respect to **'model'**.

I will start with determining the popularity of particular Mercedes models in the secondary market:"""
)

models_count = data['model'].value_counts(sort=True)
plt.rcParams["figure.figsize"] = (12,5)
plt.xlabel("model")
plt.ylabel("quantity")
plt.title("Mercedes-Benz cars on sale")
plt.bar(models_count.index, models_count, color='Darkgray')

st.pyplot(plt.gcf())
plt.close()

st.markdown("Exact values:")
st.dataframe(
    pd.DataFrame({
        'model': models_count.index,
        'quantity': models_count.values
    },
    index=range(models_count.shape[0])
    )
)

st.markdown("Let me take 3 outstandingly popular models, namely C, A and E, and illustrate their price against the year of registration.")

cea = data[(data['model'] == "C") | (data['model'] == "E") | (data['model'] == "A")]
cea = cea.loc[:, ['model', 'year', 'price']]

sns.catplot(data=cea, kind='strip', y='price', x='year', hue='model', aspect=2).set(
    title='C,E,A-Class price vs. year'
)
st.pyplot(plt.gcf())
plt.close()

st.markdown("I can see that A-Class is generally cheaper than E and C, while E-Class and C-Class are in approximately the same price range each year. However, there is a strange \"cloud\" of expensive A-Classes, their prices are considerably above the bulk. I will observe the correspondent slice:")

extreme_a = data[(data['model'] == "A") & (data['price'] > 55000)]
st.markdown(f"_Shape: {extreme_a.shape[0]} rows, {extreme_a.shape[1]} columns_")
st.dataframe(extreme_a)

st.markdown("Judging by 'mpg', 'engineSize' and 'fuelType' these are classy powerful AMG models. Thus, the price is comparably high.")
st.markdown("I will continue by identifying **how much do each model cost on average**, also taking mean engine size into account. I will take into consideration only latest models (2019 and 2020), because of age gaps and the fact that over time borders between models are being erased due to mileage.")

n = data[data['year'] > 2018].loc[:, ['model', 'price', 'engineSize']]
models = data['model'].unique()
all_mean_prices = pd.DataFrame({
    "model": models,
    "mean price": pd.Series(n[n['model'] == x]['price'].mean() for x in models),
    "engineSize": pd.Series(n[n['model'] == x]['engineSize'].mean() for x in models),
}).dropna()
all_mean_prices['mean price'] = all_mean_prices['mean price'].apply(math.ceil)
all_mean_prices = all_mean_prices.sort_values('mean price')

plt.rcParams["figure.figsize"] = (12,6.5)
sns.scatterplot(
    all_mean_prices, x='model', y='mean price', size='engineSize',
    hue='model',
    sizes=(500, 3000),
    legend=False).set(title='Mercedes-Benz cars\' mean price vs. model vs. engine size')

st.pyplot(plt.gcf())
plt.close()

st.markdown("'model'-'price' and 'model'-'engineSize' relations are distinct. Previously recognized 'engineSize'-'price' correlation is proved. It is worth mentioning that engine size becomes extremely significant contributor to the price in the slice of 2019-2020 years:")

st.dataframe(
    data[data['year'] > 2018].loc[:, ['price', 'engineSize']].corr()
)
st.markdown("_(2019-2020 engineSize'-'price' correlation)_")

st.markdown("Final piece of analysis I want to conduct is dependence between 'fuelType' and 'mpg':")

fuelmpg = data.loc[:, ['fuelType', 'mpg']]
sns.catplot(data=fuelmpg, kind='strip', x='fuelType', y='mpg', hue='fuelType').set(
    title='Mercedes cars\' fuel type vs. mpg'
)
st.pyplot(plt.gcf())
plt.close()

st.markdown("Hybrid models on average can go far more on one galoon of fuel, because it is not their only source of power. In turn, diesel is meanly **38.76%** more economical than petrol.")


# HYPOTHESIS CHECKING
st.markdown("## Hypothesis Checking")
st.markdown(
    """My hypothesis is rather simple and is as follows.

As I have previously discovered, G models have an outstandingly high mean price comparing to others, but what I also know is that price negatively correlates with 'mpg', which in turn is more or less associated with Petrol fuel type as I have just shown.

Hence, I claim that most of G-Class cars presented in the dataset work on petrol, rather then diesel or electricity. Moreover, such considerable gap in price regarding other models might indicate these Gs are powerful ones, which implies they have big engine sizes.

So, let me validate my assumptions:"""
)

g = data[data['model'] == 'G']
st.markdown(f"_Shape: {g.shape[0]} rows, {g.shape[1]} columns_")
st.dataframe(g)

st.markdown(r"Indeed, I can distinctively see my logical chain takes place and 67% of G models have petrol-powered engines. 33%, 53%, 13% of them are of size 3.0, 4.0 and 5.5 respectively, which are conventionally high values.")
