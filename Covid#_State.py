#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[77]:


url= "https://www.worldometers.info/coronavirus/country/us/"
page=requests.get(url).text
#soup = bs(page.text, 'lxml')
soup = BeautifulSoup(page,'html.parser')
#table_data = soup.find('table', class_ = 'table#usa_table_countries_today.table.table-bordered.table-hover.table-responsive.usa_table_countries.dataTable.no-footer')



# Cleaning Data from Worldometers

# In[78]:


my_table = soup.find('tbody')
table_data = []

for row in my_table.findAll('tr'):
    row_data = []
    for cell in row.findAll('td'):
        row_data.append(cell.text)
    if(len(row_data) > 0):
        data_item = {"State": row_data[1],
                     "TotalCases": row_data[2],
                     "TotalDeaths": row_data[4],
                     "ActiveCases": row_data[7],
                     "Totcase1M": row_data[8],
                     "Totdeath1M": row_data[9],
                     "TotalTests": row_data[10],
                     "Tottest1M": row_data[11],
        }
        table_data.append(data_item)
        
df = pd.DataFrame(table_data)
df = df.replace('\n','', regex=True)
df = df[1:]
#df=df.sort_values('State')
print(df)


# In[37]:


#Archives Data


# In[79]:


url2= "https://en.wikipedia.org/wiki/List_of_current_United_States_governors"
page2=requests.get(url2).text

soup2 = BeautifulSoup(page2,'html.parser')



# In[80]:


my_table2 = soup2.find('table',{'class':"wikitable"})
table_data2 = []

for row in my_table2.findAll('tr'):
    row_data = []
    for cell in row.findAll('td'):
        row_data.append(cell.text)
    if(len(row_data) > 0):
        data_item = {"State": row_data[0],
                     "Party": row_data[4],
        }
        table_data2.append(data_item)
        
print(df2)


# In[71]:


#df2['State']=df2['State'].astype('str').astype('int')
df['State']=df['State'].astype(str)
#df2['Party']=df2['Party'].astype(str)
#df=df.convert_dtypes().dtypes


# In[69]:


print(df.dtypes)
print(df2.dtypes)


# In[74]:


#full=df.set_index("State").join(df2.set_index("State"))
full=df2.merge(df,how='right',on='State')
print(full.dtypes)


# In[84]:


df.to_csv('/Users/benkelly/Downloads/Projects/COVID Overview/Data/UScovid.csv')
df2.to_csv('/Users/benkelly/Downloads/Projects/COVID Overview/Data/USparties.csv')

