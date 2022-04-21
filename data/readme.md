
# Data

**Source Data**

These 4 data are our original datasets, other data are derived from these 4.

1. netflix_titles.txt

movie and TV show data with actor, director and description information

2. rating_1.csv

This is user rating data. For successfully implementing all functionalities in this repo, you also need download this data : rating_1.csv (https://drive.google.com/file/d/1-1itMvGcMQw9Ism1BSasKnwO3m_rDFQi/view?usp=sharing). Since this dataset is too large, we only provide the link to download instead of uploading it to github.

3. movie_titles.txt

It provides information of movie_id and movie_title 

4. country_code.csv

It provides information of country name and its associated code, for map visualization



**Generated Data**

The below data are generated from the above 4 datasets.

1.net_inf

this is the common neighbors recommendation dataset, used for streamlit app

2.svd.midel

this is the trained model with parameter, used for streamlit app

3.eda.csv

this is the cleaned and feature engineered data, used for eda

4.kol.txt

this is the data containing information of users who rated much more movies than others, we call them key opinion leaders.

5.map_vis.csv

This is the aggregated data for generating heatmap

6.movie_rating.csv

This is the merged dataset from rating_1.csv and movie_title.csv, used for streamlit app.



