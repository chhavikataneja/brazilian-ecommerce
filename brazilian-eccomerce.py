# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 14:09:05 2018

@author: Yugant
"""

import csv
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline
import plotly
import plotly.plotly as py
import os
from wordcloud import WordCloud
from PIL import Image
os.chdir(r"G:\Projects\brazilian-ecommerce")
df= pd.read_csv("olist_classified_public_dataset.csv")
df2= pd.read_csv("geolocation_olist_public_dataset.csv")

df.head(10)

#Product Category Count Plot
translate_df= pd.read_csv("product_category_name_translation.csv")
translate_df.head()



#product categories names are translated into english
for i in range(0, len(translate_df)):
    df.product_category_name[df.product_category_name==translate_df.iloc[i,0]]=translate_df.iloc[i,1]
    

plt.figure(figsize=(5,8))
sns.countplot(y=df.product_category_name,orient="v")
plt.yticks(fontsize=8)
plt.xticks(fontsize=10)
plt.ylabel("Product Category Name", fontsize=12)
plt.xlabel("Product Count",fontsize=12)
plt.title("Product Category Count",fontsize=15)
plt.show()




#Product Category WordCloud
soup= ' '.join(df.product_category_name)
#wordcloud = WordCloud().generate()
wordcloud = WorldCloud(width=100,height=50,max_words=25)
wordcloud.generate(soup)
plt.figure(figsize=(10,5),facecolor='k')
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()


df.head()

# convert data types of date columns into pd.datetime
time_columns = ['order_purchase_timestamp','order_aproved_at','order_estimated_delivery_date','order_delivered_customer_date']
for i in time_columns:
    df[i]=pd.to_datetime(df[i])
df[i]



#calculate time delay between approving purchase
# calculate time gap between estimated delivery date and actual ordered date
df['approved_delay'] = df['order_aproved_at']-df['order_purchase_timestamp']
df['delivery_gap_btw_est_act'] = df['order_delivered_customer_date']-df['order_estimated_delivery_date']

# convert time delay between approving purchase into minutes data
approved_time= pd.DatetimeIndex(df['approved_delay'])
approved_minutes= approved_time.hour*60 + approved_time.minute


plt.figure(figsize=(8,3))
ax = plt.subplot(1,1,1)
sns.distplot(list(approved_minutes),color='c')
ax.set_xticks(range(0,1800,60))
plt.title("Approval Time Delay Histogram",fontsize=14)
plt.xlabel("Approval Delay in minutes", fontsize=8)
plt.show()


Deliver_gap = pd.DatetimeIndex(df['delivery_gap_btw_est_act'])
Deliver_gap= Deliver_gap.day-1

Cleaned_list= [x for x in Deliver_gap if str(x)!='nan']


#approved minutes into Histogram

plt.figure(figsize=(8,3))

sns.distplot(Cleaned_list,bins=50,color='blue')
plt.title("Time gap between Estimated Delivery Date and Actual Date"+"\n (Days Faster than estimated)",fontsize=10)
plt.xlabel("Dates",fontsize=8)
plt.show()

    

#Showing Geo Locations based on Zip code
df2= pd.read_csv("geolocation_olist_public_dataset.csv")
mapbox_access_token='pk.eyJ1IjoibGVlZG9oeXVuIiwiYSI6ImNqbjl1Y2hmcTB6dTQzcnBiNDZ2cXcwbGEifQ.hcPVtUhnyzXDXZbQQH0nMw'
data = [go.Scattermapbox(
    lon = df2['lng'],
    lat = df2['lat'],
    marker = dict(
        size = 3,
        
    ))]

layout = dict(
        title = 'Geo Locations based on Zip code',
        mapbox = dict(
            accesstoken = mapbox_access_token,
            center= dict(lat=-20,lon=-60),
            bearing=5,
            pitch=5,
            zoom=2.3,
        )
    )
fig = dict( data=data, layout=layout )
iplot( fig, validate=False)
