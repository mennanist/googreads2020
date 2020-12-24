
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import nltk
#%matplotlib inline
    
st.markdown(
    """
<style>
.e1fqkh3o1 , .e1fqkh3o1 .eknhn3m2 {
    background-image: linear-gradient(#ff8c8c,#ff4b4b );
    color: white;
}
</style>
""",
    unsafe_allow_html=True,
)

img = st.image("header.jpg", add_headers=True)
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>YOUR 2020 IN BOOKS</h1>", unsafe_allow_html=True)
st.sidebar.markdown(
"welcome! to extract your Goodreads data, all you have to do is go to 'My Books' > scroll down to find 'Tools' to your left > click 'Import and export' > 'Export Library'"
)
st.sidebar.write(" ")
st.sidebar.write(" ")

st.sidebar.markdown(
    """
<style>
.effi0qh0 {
    color: white;
}
</style>
""",
    unsafe_allow_html=True,
)

uploaded = st.file_uploader('Upload Your Goodreads data!' , type = "csv")

if uploaded is not None:
    data = pd.read_csv(uploaded)
    data = data[data['Read Count'] != 0]
    data_needed = data[['Book Id', 'Title', 'Author', 'My Rating', 'Average Rating', 'Publisher', 'Number of Pages', 'Year Published', 'Date Read', 'Bookshelves']]
    dataneeded = data_needed[data_needed['Date Read'].notnull()]
    data2020 = dataneeded[dataneeded['Date Read'].str.contains('2020/')]
    data2020['Bookshelves'].replace(np.nan, "not categorized")
    genre_count = data2020['Bookshelves'].str.split(", ", expand = True).stack().value_counts()
    genre_names = genre_count.index

    data_needed['Bookshelves'].replace(np.nan, "not categorized")
    genre_count2 = data_needed['Bookshelves'].str.split(", ", expand = True).stack().value_counts()
    genre_names2 = genre_count2.index


    sel = st.sidebar.selectbox("We're displaying 2020 data, do you want an overview of your all-time reading habits?", ('2020', 'I want it all'))
    if sel == '2020':
        st.header("Analyzing {} Books ".format(len(data2020)))
        st.text("")
        st.text("")
        st.text("")
        rating_count = data2020['My Rating'].value_counts().sort_values(ascending = False)
        st.subheader("You have rated {} books 5 stars!".format(rating_count[5]))
        fig1 = px.bar(rating_count, color = rating_count.index, labels = {"value":"Number of Books", "index":"My Rating"})
        st.plotly_chart(fig1)
        rate2020 = data2020['My Rating'].agg('mean')
        st.write("Your average rating for this year is {}! you're basically a pro!".format(round(rate2020, 2)))
        st.text("")
        st.text("")
        st.text("")

        st.subheader("Let's see how your reading habits progressed as the months went by: ")
        data2020.loc[:,'Date Read'] = pd.to_datetime(data2020['Date Read'])
        x = data2020['Date Read'].dt.month.value_counts().sort_index()
        fig2 = px.line(x=x.index, y = x, labels={"x" : "Month", "y" : "Number of Books"}, range_x=(1, 12))
        st.plotly_chart(fig2)

        fig3 = px.histogram(data2020, x='Date Read')
        st.plotly_chart(fig3)
        st.write("Looks like you've had a busy year!")
        st.text("")
        st.text("")
        st.text("")

        st.subheader("Now, your authors of the year are...")
        author2020=data2020.Author.value_counts().sort_values(ascending = False)[:5]
        authorindex = author2020.index[:5]
        fig5 = px.bar(x= authorindex, y = author2020, color=authorindex, labels={"x" : "Author", "y" : "Number of Books"}, )
        st.plotly_chart(fig5)
        st.write("either you enjoyed the works of {forst}, {secnd} and {thrd} or you were trash reading, which is fine!".format(forst = author2020.index[0], secnd = author2020.index[1], thrd = author2020.index[2]))
        st.write(" ")
        st.write(" ")

        st.subheader("Lastly, do you shelf your books into different genres/shelves?")
        ido = st.radio("Do you shelf your books into different genres/shelves?", ('Yeah', 'No...'))

        if ido == 'Yeah':
            st.subheader("Your Favorite Genre is {}".format(genre_names[0]))
            fig = px.bar(genre_count[:10], color= genre_count[:10].index, orientation="h", color_continuous_scale="Bluered_r", labels = {"value": "Number of Books Read", "index": "Shelf Name"})
            st.plotly_chart(fig)
            st.subheader("You also seem to enjoy {fir} and {sec}!".format(fir = genre_names[1], sec = genre_names[2]))

        if ido == 'No...':
            st.write("well... shelf them next year to make my job easier, nerd.")

    if sel == "I want it all":
        st.header("Analyzing {} Books ".format(len(data_needed)))
        st.text("")
        st.text("")
        st.text("")
        rating_count = data_needed['My Rating'].value_counts().sort_values(ascending = False)
        st.subheader("You have rated {} books 5 stars!".format(rating_count[5]))
        fig1 = px.bar(rating_count, color = rating_count.index, labels = {"value":"Number of Books", "index":"My Rating"})
        st.plotly_chart(fig1)
        rateall = data_needed['My Rating'].agg('mean')
        st.write("Your average rating of all time is {}!".format(round(rateall, 2)))
        st.text("")
        st.text("")
        st.text("")

        st.subheader("Let's see how your reading habits progressed as the years went by (note that only books with dates added will appear): ")
        dataneeded.loc[:,'Date Read'] = pd.to_datetime(dataneeded['Date Read'])

        x2 = dataneeded['Date Read'].dt.year.value_counts().sort_index()
        fig4 = px.line(x=x2.index, y = x2, labels={"x" : "Year", "y" : "Number of Books"})
        st.plotly_chart(fig4)
        st.write("Wow...")
        st.text(" ")
        st.write(" ")

        st.subheader("Now, your favorite author of all time is...")
        authoralltime=data_needed.Author.value_counts().sort_values(ascending = False)[:10]
        authorindex = authoralltime.index[:10]
        fig5 = px.histogram(x= authorindex, y = authoralltime, color=authorindex, labels={"x" : "Author", "y" : "Number of Books"})
        st.plotly_chart(fig5)
        st.write("either {forst}, {secnd} and {thrd} are your favorite authors or you simply hate yourself!".format(forst = authoralltime.index[0], secnd = authoralltime.index[1], thrd = authoralltime.index[2]))
        st.write(" ")
        st.write(" ")


        st.subheader("Lastly, do you shelf your books into different genres/shelves?")
        ido = st.radio("Do you shelf your books into different genres/shelves?", ('Yeah', 'No...'))

        if ido == 'Yeah':
            st.subheader("Your Favorite Genre of all time is {}".format(genre_names2[0]))
            fig = px.bar(genre_count2[:10], color= genre_count[:10].index, orientation="h", color_continuous_scale="Bluered_r", labels = {"value": "Number of Books Read", "index": "Shelf Name"})
            st.plotly_chart(fig)
            st.subheader("You also seem to enjoy {fir} and {sec}!".format(fir = genre_names2[1], sec = genre_names2[2]))
        if ido == 'No...':
            st.write("well... again, shelf them next year to make my job easier, nerd.")



    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown("<h3 style='text-align: center; color: #ff4b4b;'>Thank you, that's it for this year!</h3>", unsafe_allow_html=True)


    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")

    st.text("Note that:")
    st.write("- Goodreads has some issues with csv exports and dates so the number of books might not be your 2020 total, you'll know just how many titles were analyzed!")
    st.write("Contact me: mennaoessam2@gmail.com")