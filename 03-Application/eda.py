import streamlit as st
# from PIL import Image
# import cv2 
import pandas as pd
import numpy as np
import os
import random
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit.components.v1 as components
def show_map(input_type,df):
    # if input_year!='all':
    #     df = df[df.release_year==input_year]
    if input_type!='all':
        df = df[df.type==input_type]
    if input_type == 'all':
        color_ = 'greens'
    if input_type == 'TV Show':
        color_ = 'blues'
    if input_type == 'Movie':
        color_ = 'oranges'

    count = df.groupby(['release_year',"new_code"]).count().reset_index().rename(columns ={"type":"count"})
    avg_count = count['count'].values.mean()
    fig = px.choropleth(count, locations="new_code",
                        color="count", # lifeExp is a column of gapminder
                        hover_name="new_code", # column to add to hover information
                        animation_frame="release_year",
                        # color_continuous_midpoint=avg_count,
                        range_color = [count['count'].values.min(),count['count'].values.max()],
                        # color_continuous_scale=px.colors.sequential.Plasma
                        color_continuous_scale=color_
                        
                        )
    if input_type=='all':
        input_type = 'TV show and Movie'
    fig.update_layout(
    title_text='Global %s Heatmap'%input_type)
    st.plotly_chart(fig)



        
    
def load_image(image_path,title='',subheader='',width=100):
    
    st.title(title)  
    st.subheader(subheader)
    print(image_path)
    st.image(image_path,width)

def show_trend(df1_pd):
    df_ = df1_pd[df1_pd['type'] == 'TV Show'].groupby('release_year').count()[-25:-1]
    df1_ = df1_pd[df1_pd['type'] == 'Movie'].groupby('release_year').count()[-25:-1]
    df2_ = df1_pd.groupby('release_year').count()[-25:-1]


    plt.figure(figsize = (15,8))
    sns.set_style('darkgrid')
    sns.lineplot(data = df_['show_id'],palette = 'Set1')
    sns.lineplot(data = df1_['show_id'],palette = 'Set1')
    sns.lineplot(data = df2_['show_id'],palette = 'Set1')
    plt.title('Year over Year Content Released',fontsize = 15)
    plt.xlabel('Year',fontsize = 15)
    plt.ylabel('No.of Shows',fontsize = 15)
    plt.legend(['TV', 'Movie','Total'], fontsize='large')
    st.pyplot(plt,width =2)

def TV_season(df1_pd):
    plt.figure(figsize= (7,3))
    tv_show = df1_pd[df1_pd['type']== 'TV Show']

    sns.countplot(x = 'duration',data = tv_show,palette = 'Oranges_r', order = tv_show['duration'].value_counts().index)
    plt.xticks(rotation = 0)
    plt.xlabel("Seasons",fontsize = 15)
    plt.ylabel("Total count",fontsize = 15)
    plt.title("Total Tv Show Season wise",fontsize = 15)
    st.pyplot(plt,width =2)
def movie_duration(df1_pd):
    movie_duration = df1_pd.loc[df1_pd['type']=='Movie']

    plt.figure(figsize=(12,10))

    ax = sns.histplot(data = movie_duration,x = 'duration',bins = 50,kde = True,color = 'red')
    plt.title('Movie Duration',fontsize = 15)
    plt.xlabel('Total Duration(In Mins)',fontsize = 15)
    plt.ylabel('Total Movie Count',fontsize = 15)
    st.pyplot(plt,figsize=(12,1))

    


def app():

    df_map = pd.read_csv("../data/map_vis.csv")
    df1_pd = pd.read_csv("../data/eda.csv")
    type_list = df_map.type.unique().tolist()
    year_list = sorted(df_map.release_year.unique().tolist())
    input_type = st.selectbox(
    'Which type are you interested in?',
    ['all']+type_list
    )
    # input_year = st.selectbox(
    # 'Which year are you interested in?',
    # ['all']+year_list[::-1]
    # )

    show_map(input_type,df_map)

    show_trend(df1_pd)
    TV_season(df1_pd)
    movie_duration(df1_pd)

    # HtmlFile = open("/Users/luocan/class/2021spring/big_data/final-project/vis/actor.html", 'r', encoding='utf-8')
    # source_code = HtmlFile.read() 
    # components.html(source_code, height = 1500,width=1000)








if __name__ == "__main__":
    app()