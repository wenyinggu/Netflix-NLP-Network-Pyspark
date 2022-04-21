import eda
import recommend
import ent_network
import rec_new
# import rec_old
import streamlit as st



st.set_page_config(layout='wide')
st.markdown("""
<style>
.normal-font {
    font-size:50px !important;
    font-family:  "Copperplate";
    color:#F7F5F5;
    text-align: center;
}
.big-font {
    font-size:120px !important;
    font-family:  "Copperplate";
    color:#9F1F04;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="normal-font">Get your Best Experience on </p>', unsafe_allow_html=True)
st.markdown('<p class="big-font">NETFLIX</p>', unsafe_allow_html=True)
st.markdown(
    """
    <style>
    .reportview-container {

        background: url("https://store-images.s-microsoft.com/image/apps.19703.9007199266246365.73e47f2a-59d9-4ab9-a337-947a9821644b.42888798-183a-4256-84f6-5c10020990b3?mode=scale&q=90&h=720&w=1280");

    }
   .sidebar .sidebar-content {
        background: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366")
    }
    </style>
    """,
    unsafe_allow_html=True
)
PAGES = {
    "A glance of NETFLIX": eda,
    "Content based recommendation": recommend,
    'User based recommendation': rec_new,
    "Take a peek at NETFLIX Network": ent_network
    
    # 'Recommend for old user': rec_old

}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()

#https://www.google.com/imgres?imgurl=https%3A%2F%2Fi.insider.com%2F5f9c88816f5b310011
#724a26&imgrefurl=https%3A%2F%2Fwww.businessinsider.com%2Fhow-much-is-netflix&tbnid=FmvzovMIteeiJM&v
#et=12ahUKEwiB_r7fjZfwAhUSVt8KHbdlDC0QMygTegUIARD4AQ..i&docid=2q8pKGAfvaUvPM&w=2996&h=1498&q=net
#flix&ved=2ahUKEwiB_r7fjZfwAhUSVt8KHbdlDC0QMygTegUIARD4AQ