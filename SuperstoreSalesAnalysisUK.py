#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
import numpy as np
import datetime
import plotly.express as px
import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)


# In[53]:


#Reading the file and saving it in a pandas dataframe
SuperstoreSales = pd.read_csv('SuperstoreSalesUK.csv', encoding= 'unicode_escape', parse_dates=True)
SuperstoreSales.head()


# In[79]:


#check for missing values

print(SuperstoreSales.isna().any())
# We observe null values in the Postal Code field of the data. Let's evaluate the number of null values in this field.

print(SuperstoreSales.isna().sum())

# Counting the number of null values, we see all the orders have null values for Postal Code. 
# This field is not very important for our analysis, deleting this column along with the row ID, Market and Region
del SuperstoreSales['Row ID']
del SuperstoreSales['Postal Code']
del SuperstoreSales['Market']
del SuperstoreSales['Region']

SuperstoreSales.info()


# In[68]:


#correcting date format

SuperstoreSales['Order Date'] = pd.to_datetime(SuperstoreSales['Order Date'], errors ='coerce', dayfirst=True)
SuperstoreSales['Ship Date'] = pd.to_datetime(SuperstoreSales['Ship Date'], errors ='coerce', dayfirst=True)
format = "%Y/%m/%d"
SuperstoreSales.info()
SuperstoreSales.head()


# In[69]:


#Finding unique instances of all fields
SuperstoreSales.nunique()


# In[70]:


# Dataframe at a glance. 
SuperstoreSales.describe()


# In[71]:


# Store's performance in terms of total sales, quantity and profit

print("The total sales recorded is :",round(sum(SuperstoreSales['Sales']), 0))
print("The total quantity sold is is :",round(sum(SuperstoreSales['Quantity']), 0))
print("The total profit made by the store is :",round(sum(SuperstoreSales['Profit']), 0))


# In[72]:


#Top 10 cities by Sale
# sorting city- wise aggregated sum of sales.

df_SaleTop10=SuperstoreSales.groupby('City')['Sales'].sum().reset_index()
df_SaleTop10sorted = df_SaleTop10.sort_values('Sales',ascending=False).head(10)
df_SaleTop10sorted

#Plotting the data
sns.barplot(x='City', y='Sales', data=df_SaleTop10sorted, palette='ocean_r')
plt.xticks(rotation=90, fontsize = 12)
plt.yticks(fontsize = 12)
plt.title('Top 10 cities by Sales');


# In[73]:


#Top 10 cities by Profit
# sorting city- wise aggregated sum of profit.

df_ProfitTop10=SuperstoreSales.groupby('City')['Profit'].sum().reset_index()
df_ProfitTop10sorted = df_ProfitTop10.sort_values('Profit',ascending=False).head(10)
df_ProfitTop10sorted

#Plotting the data
sns.barplot(x='City', y='Profit', data=df_ProfitTop10sorted, palette='ocean_r')
plt.xticks(rotation=90, fontsize = 12)
plt.yticks(fontsize = 12)
plt.title('Top 10 cities by Profit');


# In[74]:


SuperstoreSales.head()


# In[157]:


#Sub-category level Sales and profit

colormap = ['navy', 'Teal']
plt.rcParams["figure.figsize"] = (10,4)
fig = SuperstoreSales.groupby('Sub-Category')['Sales','Profit'].agg(['sum']).plot.bar(color=colormap)
plt.title('Sub-Category level total Sales & Profit')
plt.legend(loc=2, title='Legend');


# In[158]:


# Correlation heatmap
fig, ax = plt.subplots(figsize=(10,3))
# sns.set()
sns.heatmap(np.round(SuperstoreSales.corr(),2),annot=True, cmap='Blues')
plt.yticks(rotation=360)
plt.title('Correlation matrix');


# In[159]:


#Summarizing the data yearly
SuperstoreSales['Year'] = SuperstoreSales['Order Date'].apply(lambda x: x.strftime('%Y'))

year =  [*range(2011, 2015, 1)]
dfYear = pd.Series(year)

YoYSale = (SuperstoreSales.groupby(['Year'])['Sales'].sum())
YoYQuantity = round(SuperstoreSales.groupby(['Year'])['Quantity'].sum(),0)
YoYProfit = round(SuperstoreSales.groupby(['Year'])['Profit'].sum(),0)
YoYShippingCost = round(SuperstoreSales.groupby(['Year'])['Shipping Cost'].sum(),0)
YoYOrders = round(SuperstoreSales.groupby(['Year'])['Order ID'].nunique(),0)
YoYCustomers = round(SuperstoreSales.groupby(['Year'])['Customer ID'].nunique(),0)
YoYDiscount = round(SuperstoreSales.groupby(['Year'])['Discount'].mean(),4)

YoY = pd.concat([YoYSale, YoYQuantity, YoYProfit, YoYShippingCost,YoYOrders,YoYCustomers,YoYDiscount], axis=1).reset_index()
# YoY.set_index('Year')
YoY


# In[164]:


YoYGrowth = YoY.copy()
YoYGrowth['No._of Orders'] = YoY['Order ID']
YoYGrowth['No._of Customers'] = YoY['Customer ID']
pct = YoYGrowth[['Sales','Quantity', 'Profit', 'Shipping Cost', 'No._of Orders', 'No._of Customers']].astype(float).pct_change()
pct['Year'] = YoY['Year']
YoYGrowth2 = pct.set_index('Year')
YoYGrowth2.style.format("{:.2%}")


# In[160]:


#Analysing yearly Sales behaviour with discount

fig,ax = plt.subplots()
ax.plot(YoY.Year, YoY.Sales, color="red", marker="o")
ax.set_title("Twin plots")
ax.set_xlabel("year",fontsize=14)
ax.set_ylabel("Sales",color="red",fontsize=14)

ax2=ax.twinx()
# twinx() to help us make a plot with two different y axis
ax2.plot(YoY['Year'], YoY['Discount'], color="black",marker="o")
ax2.set_ylabel("Discount%",color="black",fontsize=14)
plt.show()


# In[161]:


# Multilevel hierarchical Sales Composition

fig = px.sunburst(SuperstoreSales,path=['Country','Segment','Category', 'Sub-Category'], values='Sales', color='Sales', color_continuous_scale='blues')
fig.update_traces(insidetextorientation='radial')
fig.show()


# In[102]:


#Analysing the numerical distribution

numeric_fields = ['Sales', 'Profit', 'Quantity', 'Shipping Cost', 'Discount']
ax_list= SuperstoreSales[numeric_fields].hist(bins=15,figsize=(10, 10), layout=(3, 2), grid=False, color="navy")


# In[18]:


# Segment wise Sales - Profit mix.

plt.rcParams["figure.figsize"] = (10,7)
sns.scatterplot(x='Sales', y='Profit', data = SuperstoreSales, hue='Segment', style='Segment', palette='ocean')
plt.title('Sales and Profit', fontsize = 15)
ax.set_xlabel('Sales')
ax.set_ylabel('Profit');


# In[57]:


# Analysing ship modes with Order Priority  

plt.figure(figsize=(10, 4))
sns.countplot(x=SuperstoreSales['Ship Mode'], hue='Order Priority', data=SuperstoreSales, palette="ocean")
plt.title("Ship Mode Analysis")
plt.xticks(size=10)
plt.legend(loc=1)
sns.color_palette("flare", as_cmap=True);


# In[91]:


#Purchase patterns

plt.figure(figsize=(11, 5))
sns.countplot(x=SuperstoreSales['Segment'], hue='Sub-Category', data=SuperstoreSales, palette ="rocket_r")
plt.title("Purchase patterns")
plt.xticks(size=10)
plt.legend(bbox_to_anchor=(1, 1),borderaxespad=1);


# In[166]:


#Pareto analysis
#Calculate TotalPrice Per Product and sort them by the products with the highest Sales.
SuperstoreSalesProduct = SuperstoreSales.groupby('Product Name').agg({'Sales': 'sum'}).sort_values('Sales', ascending=False)
SuperstoreSalesProduct.reset_index(inplace=True)
SuperstoreSalesProduct.head()


# In[167]:


# #Finding the Total Sales 
SuperstoreSalesProduct["Sales"].sum()


# In[168]:


#Finding the cumulative total of the sorted products 
SuperstoreSalesProduct['SumTotalPrice'] = SuperstoreSalesProduct.Sales.cumsum()
SuperstoreSalesProduct.head()


# In[169]:


#Defining a variable to hold the threshold value. 
threshold = SuperstoreSalesProduct["Sales"].sum() * 0.80

#Using subsetting to find the products that make up 80% of the total Sales and storing it in a ariable
SuperstoreSalesProduct80perc = SuperstoreSalesProduct[SuperstoreSalesProduct['SumTotalPrice'] <= threshold]
SuperstoreSalesProduct80perc


# In[170]:


SuperstoreSalesProduct80perc["Product Name"].nunique()
#All the products in the Dataframe are hence unique


# In[171]:


# Finding percentage of products contributing to top 80% Sales. We see that a relatively small subset of 30% (although not 20%) 
# of all products contribute to top 80% Sales thereby confirming our analysis.
SuperstoreSalesProduct80perc["Product Name"].nunique()/SuperstoreSalesProduct["Product Name"].nunique()

