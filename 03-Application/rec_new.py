import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import streamlit as st
from scipy.stats import pearsonr
import pyspark
from pyspark.sql import *
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark import SparkContext, SparkConf
from pyspark.ml.recommendation import ALS, ALSModel


df = pd.read_csv("../data/rating_1.csv")
mov = pd.read_csv("../data/movie_titles1.txt",sep='\t')

mov_rating =  pd.read_csv("../data/movie_rating.csv")

def load_image(image_path,title='',subheader='',width=50):
    
    st.title(title)  
    st.subheader(subheader)
    print(image_path)
    st.image(image_path,width=200)


def survey_for_new_user(n):

    st.title("Please rate the following movie so that we can customize your movie recommendation")
    df_k = pd.read_csv('../data/kol.txt')
    movie_ids = df_k.columns[1:n+1]
    movie_ids = np.array([int(mid) for mid in movie_ids])
    # st.text(str(movie_ids))
    try:
        # st.text(str(list(movie_ids)))
        name_list = mov.name.values[movie_ids-1]
    except:
        # st.text("?")
        name_list = []
    rating_list = [0]*n

    # st.text(str(name_list))
    for i in range(len(name_list)):
        # st.text(name_list[i])
        mov_dir='movie_pic/'+name_list[i].replace(' ','_')
        # st.text(mov_dir)
        for mov_name in os.listdir(mov_dir):
            if mov_name[-5:]=='.jpeg':
                # st.text(mov_dir+'/'+mov)
                load_image(mov_dir+'/'+mov_name,title = name_list[i])
                # rec_pic.append(mov_dir+'/'+mov)
                break
        # rating =st.text_input("give a rating from 1 to 5",key=i)
        rating = st.selectbox("Your rating: ",list(range(1,6)),key = i)
        
        rating_list[i] = rating
    return(movie_ids,rating_list)
def rec_movie_for_old_user(user_id,k):
    df_user = df[df.user_id == user_id]
    pos_movie =list( set(list(range(1,4500)))-set(df_user.movie_id.values))
    df_pred = pd.DataFrame({'user_id':user_id, 'movie_id': pos_movie})

    # create the session
    conf = SparkConf().set("spark.ui.port", "4050")
    # create the context
    sc = pyspark.SparkContext.getOrCreate(conf=conf)
    spark = SparkSession.builder.getOrCreate()
    persistedModel = ALSModel.load('../data/svd.model')
    dfs = spark.createDataFrame(df_pred)
    predictions_new = persistedModel.transform(dfs)
    pred = predictions_new.orderBy('prediction',ascending=False).toPandas().head(k)
    sc.stop()
    pred = pred.merge(mov)
    return pred


def rec_for_new(rating_list,k):
    rating_list=[int(r) for r in rating_list]
    df_k = pd.read_csv('../data/kol.txt')
    cor_old = -1
    sim_user = 0
    for line in df_k.values:
        rating_vec = line[1:len(rating_list)+1]
        corr = pearsonr(rating_vec,rating_list)[0]
        if corr>cor_old:
            sim_user = line[0]
            cor_old = corr
        if corr>0.85:
            break
#     print(cor_old)
    pred = rec_movie_for_old_user(sim_user,k)
    return pred



def app():
    selected_box = st.sidebar.selectbox(
    'Who are you?',
    ('Old user','New user')
    )
    if selected_box=='New user':
        st.sidebar.text("Since you are new user, we need do a short survey to know your taste :)")
        # survey_num = int(st.sidebar.number_input("How many movies do you want to rate now: "))
        survey_num = st.sidebar.selectbox("How many movies do you want to rate now: ",list(range(1,21)))
        # k = int(st.sidebar.number_input("How many movies do you want us to recommend: "))
        k = st.sidebar.selectbox("How many movies do you want us to recommend: ",list(range(1,21)))
        movie_id_list,rating_list = survey_for_new_user(survey_num)
        
        if st.button('Recommend'): 
            pred = rec_for_new(rating_list,k)
            st.text("You might like:")
            st.dataframe(pred)
    elif selected_box=='Old user':
        sample_user = sorted(df.user_id.unique().tolist()[:20])
        user_id = st.sidebar.selectbox("Your user ID: ",sample_user)

        # k = int(st.sidebar.number_input("How many movies do you want us to recommend: "))
        k = st.sidebar.selectbox("How many movies do you want us to recommend: ",list(range(1,21)))
        if st.button('Recommend'): 
            pred = rec_movie_for_old_user(user_id,k)
            st.text("Based on your historical rating, you might like:")
            st.dataframe(pred)




    

if __name__ == "__main__":
    app()
