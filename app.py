# Import Libraries
import requests
import pprint
import pandas as pd
from collections import Counter
import streamlit as st
import plotly.express as px
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
pp = pprint.PrettyPrinter()
st.set_option('deprecation.showPyplotGlobalUse', False)



df = pd.read_csv("Jobs-Web3.careers.csv")
count_tags_df = pd.read_csv('tags_df.csv')
df.fillna('Null', inplace=True)

master_list = []
for sublist in df['tags']:
    arr = sublist.split(',')
    for element in arr:
        master_list.append(element)

count_tags = Counter(master_list)

count_tags_df = pd.DataFrame.from_dict(count_tags, orient='index',columns = ['count']).reset_index()
count_tags_df.sort_values(by = 'count',ascending = False,inplace = True)
count_tags_df = count_tags_df.iloc[0:10,:].reset_index()

jobs_per_company_df = df.company.value_counts(ascending=True).rename_axis('Companies').reset_index(name='counts')

st.title(" Web3.careers data")
st.sidebar.title("Edit the charts")
jb_counts = st.sidebar.slider('Number of jobs', jobs_per_company_df.counts.min(), jobs_per_company_df.counts.max(), jobs_per_company_df.counts.min())
jobs_per_company_df.rename(columns = {'counts':'Number of jobs'}, inplace = True)


jobs_per_company_df_2 = jobs_per_company_df[jobs_per_company_df['Number of jobs']>=jb_counts]
st.markdown("## Number of jobs per companies")
fig = px.bar(jobs_per_company_df_2, x='Companies', y='Number of jobs',color='Number of jobs',color_continuous_scale=["#0ba0f7", "#1740fa","#3317ad"])
fig.update_layout(width=900,height=650)
st.plotly_chart(fig)


st.markdown('## Top 10 Tags')
count_tags_df.sort_values(by='count', ascending=True, inplace=True)
count_tags_df.rename(columns = {'index':'Tags'}, inplace = True)
count_tags_df.rename(columns = {'count':'Frequency'}, inplace = True)

fig2 = px.bar(count_tags_df, x="Frequency", y="Tags", orientation='h',color='Frequency')
st.plotly_chart(fig2)

st.markdown('## World Cloud')

cloud_text = ""
for index, row in df.iterrows():
    cloud_text += row['description']
cloud_text = cloud_text.replace('\n','')
cloud_text = cloud_text.replace('will','')
cloud_text = cloud_text.replace('CANDYSHOP','')
cloud_text = cloud_text.replace('applying','')
cloud_text = cloud_text.replace('role','')


word_cloud2 = WordCloud(collocations = False, background_color = 'white',width=1000, height=600).generate(cloud_text)

#fig3.set_size_inches(18.5, 10.5)
plt.imshow(word_cloud2, interpolation='bilinear')
plt.axis("off")
plt.show()
st.pyplot()


remote_count = []
for index, row in df.iterrows():
    if 'remote' in  row['title'] or 'Remote' in  row['title']  or 'REMOTE' in  row['title'] :
        remote_count.append(1)
        continue
    elif 'remote' in  row['company'] or 'Remote' in  row['company']  or 'REMOTE' in  row['company'] :
        remote_count.append(1)
        continue
    elif 'remote' in  row['location'] or 'Remote' in  row['location']  or 'REMOTE' in  row['location'] :
        remote_count.append(1)
        continue
    elif 'remote' in  row['tags'] or 'Remote' in  row['tags']  or 'REMOTE' in  row['tags'] :
        remote_count.append(1)
        continue
    elif 'remote' in  row['description'] or 'Remote' in  row['description']  or 'REMOTE' in  row['description'] :
        remote_count.append(1)
        continue
    remote_count.append(0)
    
df['remote_count'] = remote_count
counts = df.iloc[:,[5,6]]

remote_counts_df = counts.remote_count.value_counts().to_frame()
remote_counts_df.rename(columns = {'remote_count':'Number of Jobs'}, inplace = True)
remote_counts_df['Location'] = ['Remote', 'On-site']
st.markdown('## On-site/Remote')
fig4 = px.bar(remote_counts_df, x='Location', y='Number of Jobs',color="Location",color_discrete_sequence=["green", "blue"])
fig4.update_layout(width=900,height=650)
st.plotly_chart(fig4)



companies_job = list = df.company.unique().tolist()
st.sidebar.title("Company job offer")
companies_offering_jobs = st.sidebar.selectbox("Company:", companies_job)
st.markdown('## '+str(companies_offering_jobs)+" job openings" )

companies_offering_jobs_df = df[df['company']==companies_offering_jobs]
companies_offering_jobs_df.rename(columns = {'title':'Job Title'}, inplace = True)
companies_offering_jobs_df = companies_offering_jobs_df.iloc[:,1].reset_index().iloc[:,1]
companies_offering_jobs_df.index = np.arange(1,len(companies_offering_jobs_df)+1)

st.write(companies_offering_jobs_df)













