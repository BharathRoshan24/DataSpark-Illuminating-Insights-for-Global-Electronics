#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
from mysql.connector import Error
import numpy as np


# Load Tables

# In[5]:


sales=pd.read_csv("Sales.csv")
customers=pd.read_csv("Customers.csv", encoding='ISO-8859-1')
exchangerates=pd.read_csv("Exchange_Rates.csv")
products=pd.read_csv("Products.csv")
stores=pd.read_csv("Stores.csv")


# In[7]:


sales.isnull().sum()


# In[8]:


sales.dtypes


# In[9]:


sales['Order Date'] = pd.to_datetime(sales['Order Date'], format='%m/%d/%Y')
sales['Delivery Date'] = pd.to_datetime(sales['Delivery Date'], format='%m/%d/%Y', errors='coerce')
sales['Currency Code'] = sales['Currency Code'].astype(str)


# In[10]:


sales.fillna('Not Available', inplace=True)
sales


# In[11]:


stores


# In[12]:


stores.isnull().sum()


# In[13]:


stores.dtypes


# In[14]:


stores.fillna(0,inplace=True)


# In[15]:


stores.dtypes


# In[16]:


stores['Country']=stores['Country'].astype(str)
stores['State']=stores['State'].astype(str)
stores['Open Date']=pd.to_datetime(stores['Open Date'],format='%m/%d/%Y')


# In[17]:


stores


# In[18]:


products.isnull().sum()


# In[19]:


products.dtypes


# In[20]:


products


# In[21]:


products['Unit Cost USD'] = products['Unit Cost USD'].replace('[\$,]', '', regex=True).astype(float)
products['Unit Price USD'] = products['Unit Price USD'].replace('[\$,]', '', regex=True).astype(float)


# In[22]:


products.dtypes


# In[23]:


products


# In[24]:


customers.isnull().sum()


# In[25]:


customers.dtypes


# In[26]:


def convert_date(date_str):
    try:
        return pd.to_datetime(date_str, format='%m/%d/%Y', errors='coerce').strftime('%m/%d/%Y')
    except ValueError:
        try:
            return pd.to_datetime(date_str, format='%d-%m-%Y', errors='coerce').strftime('%m/%d/%Y')
        except ValueError:
            return date_str 
customers['Birthday'] = customers['Birthday'].apply(convert_date)


# In[27]:


customers['State Code'].fillna('Not Available', inplace=True)


# In[28]:


customers['Birthday'] = pd.to_datetime(customers['Birthday'], format='%m/%d/%Y', errors='coerce')


# In[29]:


customers


# In[30]:


exchangerates.dtypes


# In[31]:


exchangerates


# In[32]:


exchangerates['Date'] = pd.to_datetime(exchangerates['Date'], format='%m/%d/%Y', errors='coerce')


# In[33]:


exchangerates


# In[34]:


sales 


# In[35]:


customers


# In[36]:


overall=sales


# In[37]:


overall=pd.merge(overall,customers,on='CustomerKey',how='inner')


# In[38]:


overall.dropna(inplace=True)


# In[39]:


overall


# In[40]:


overall=pd.merge(overall,exchangerates,left_on=['Order Date','Currency Code'],right_on=['Date','Currency'],how='inner')


# In[41]:


overall=pd.merge(overall,products,on='ProductKey',how='inner')


# In[42]:


overall=pd.merge(overall,stores,on=['StoreKey','Country','State'],how='inner')


# In[43]:


overall


# In[44]:


col=list(overall.columns)
col1=[]
for c in col:
    col1.append(c.replace(' ','_').lower())
    
overall.columns=col1


# In[45]:


col=list(stores.columns)
col1=[]
for c in col:
    col1.append(c.replace(' ','_').lower())
    
stores.columns=col1


# In[46]:


col1


# In[47]:


overall.columns


# In[48]:


overall.isnull().sum()


# In[49]:


overall.dtypes


# In[50]:


overall[['order_date','date','currency_code','currency','customerkey']]


# In[51]:


overall.to_csv('overall.csv')


# In[57]:


import pymysql

# Establish a connection to the MySQL server
connection = pymysql.connect(
    host="localhost",
    port=3306,  
    user="root",  
    password="roshan21"
)

try:
    # Create a cursor object
    cursor = connection.cursor()

    # SQL query to create a new database
    database_name = "DataSpark"
    cursor.execute(f"CREATE DATABASE {database_name}")

    print(f"Database '{database_name}' created successfully!")

except pymysql.MySQLError as e:
    print(f"Error occurred: {e}")

finally:
    # Close the connection
    cursor.close()
    connection.close()


# In[58]:


import pandas as pd
import pymysql
from sqlalchemy import create_engine
 
host = "localhost"
port = "3306"
username = "root"
password = "roshan21"
database = "DataSpark"
 
engine_string = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(engine_string)
 
table_name = "overall"
overall.to_sql(table_name, engine,if_exists='replace',index=False)
print(f"successfully imported {table_name} to sql")

table_name = "customers"
customers.to_sql(table_name, engine,if_exists='replace',index=False)
print(f"successfully imported {table_name} to sql")

table_name = "products"
products.to_sql(table_name, engine,if_exists='replace',index=False)
print(f"successfully imported {table_name} to sql")

table_name = "exchangerates"
exchangerates.to_sql(table_name, engine,if_exists='replace',index=False)
print(f"successfully imported {table_name} to sql")

table_name = "stores"
stores.to_sql(table_name, engine,if_exists='replace',index=False)
print(f"successfully imported {table_name} to sql")


# In[ ]:




