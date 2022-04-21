import streamlit as st
import pandas as pd
import numpy as np
import os
import random
import matplotlib.pyplot as plt
import pyspark
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, RegexTokenizer
from pyspark.sql.functions import col, udf
from pyspark.sql.types import IntegerType
from pyspark.ml.feature import StopWordsRemover
from pyspark.ml.feature import Word2Vec
from pyspark.ml.feature import StandardScaler
from pyspark.ml.feature import HashingTF, IDF
from pyspark.ml.feature import Normalizer


def rec_by_content(name, df_rec,content_rec,k=5):
    name_list = df_rec.title.tolist()
    j = name_list.index(name)
    rec_name_list = content_rec[j].split('\t')
    rec_idx_list= [ name_list.index(rec_name) for rec_name in rec_name_list]
    df_rec.loc[rec_idx_list,:]

    return df_rec.loc[rec_idx_list,:].head(k)
        
def show_rec(rec_df):
    rec_df = rec_df.reset_index(drop=True).fillna("unknown")
    rec = 0
    pic_dir ='movie_pic/'
    alL_mov = os.listdir(pic_dir)
    rec_pic = []

    for i in range(rec_df.shape[0]):
        # st.text(rec_df.columns)
        rec_name = rec_df.title[i]
        rec_desc = "Director: %s\nCast: %s\nCountry/Region: %s\n"%(rec_df.director[i],rec_df.cast[i],rec_df.country[i])+\
        "Year: %d\nDescription: %s\nRating: %s\n"%(rec_df.release_year[i],rec_df.description[i],rec_df.rating[i])

        mov_dir = pic_dir+rec_name.replace(" ","_")
        show_num = 0
        try:
            for mov in os.listdir(mov_dir):
                if mov[-5:]=='.jpeg':
                    load_image(mov_dir+'/'+mov,title = "Top %d"%(i+1),subheader = rec_name)
                    st.text(rec_desc)
                    # rec_pic.append(mov_dir+'/'+mov)
                    show_num+=1
                    break
        except:
            place_holder_path = "image_place_holder/free-movie-icon-850-thumb.png"
            load_image(place_holder_path,title = rec_name,subheader = rec_desc)

    return rec
        

    
def load_image(image_path,title='',subheader=''):
    
    st.title(title)  
    st.subheader(subheader)
    print(image_path)
    st.image(image_path,width=100)

def app():

    with open( "../data/content_rec.csv","r") as f:
        content_rec = f.read().split('\n')[:-1]
    df_rec = pd.read_csv("../data/netflix_titles.txt",sep='\t')
    sample_show = df_rec.title.values[-20:]
    rec_num = st.sidebar.selectbox(
    'How many recommendation do you want?',
    list(range(1,21))
    )
    input_show = st.sidebar.selectbox(
    'Choose your favorite show here:',
    sample_show
    )
    if rec_num and input_show:
        rec_df = rec_by_content(input_show,df_rec,content_rec,int(rec_num))
        show_rec(rec_df)




if __name__ == "__main__":
    app()