import streamlit as st
# from PIL import Image
# import cv2 
import pandas as pd
import numpy as np
import os
import random
import streamlit.components.v1 as components

def get_rec(input_name,df,k=10):
    name_list = df[0].tolist()
    idx = name_list.index(input_name)
    output = df.iloc[idx,1:k+1].tolist()
#     df_rec = df[df[0]==input_name]
    return output
def show_rec(rec_list):
    pic_dir ='actor_pic/'
    alL_mov = os.listdir(pic_dir)
    rec_pic = []

    for i in range(len(rec_list)):
        # st.text(rec_df.columns)
        rec_name = rec_list[i]
        mov_dir = pic_dir+rec_name.replace(" ","_")
        show_num = 0
        try:
            for mov in os.listdir(mov_dir):
                if mov[-5:]=='.jpeg':
                    load_image(mov_dir+'/'+mov,title = "Top %d"%(i+1),subheader = rec_name)
                    show_num+=1
                    break
        except:
            place_holder_path = "image_place_holder/people-icon.png"
            load_image(place_holder_path,title = "Top %d"%(i+1),subheader = rec_name)

    return 
        
    
def load_image(image_path,title='',subheader='', width=100):
    
    st.title(title)  
    st.subheader(subheader)
    print(image_path)
    st.image(image_path,width=width)

def app():
    # try:
    view_net = st.button("View NETFLIX social network")

    if view_net:
        st.write("This is the network centered around Kevin Bacon. \nA statement here: all actors in this network is not further than 2 steps away from Kevin Bacon.\n Do you believe it?")

        # HtmlFile = open("sample.html", 'r', encoding='utf-8')
        HtmlFile = open("vis/actor.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read() 
        components.html(source_code, height = 500,width=1000)

    # load_image('/Users/luocan/class/2021spring/big_data/final-project/app/actor_net.png',
    #     title='Explore the entertainment industry network',subheader='',
    #     width = 800)

    input_cat = st.sidebar.selectbox(
    'Who are you?',
    ('actor','director')
    )

    if input_cat =='actor':
        output_cat = 'actor'
    else:
        output_cat = st.sidebar.selectbox(
        'Who are you intersted in?',
        ('actor','director')
        )
    if input_cat =='director':
        input_c = 'd'
    else:
        input_c = 'c'
    if output_cat =='director':
        output_c = 'd'
    else:
        output_c = 'c'
    path = "../data/net_inf/common_neighbor_%s%s.txt"%(input_c,output_c)
    df = pd.read_csv(path,header = None)
    name_list = df[0].tolist()
    input_name = st.sidebar.selectbox(
        'Your name: ',
        sorted(name_list)
        )
    K = st.sidebar.selectbox(
        'How many recommendation do you want? ',
        list(range(1,11))
        )

    rec_list = get_rec(input_name,df,k = K)
    st.title("Based on the common neighbors information, we think you might be intersted in these %ss"%(output_cat))
    show_rec(rec_list)







if __name__ == "__main__":
    app()