
import streamlit as st
import numpy as np, pandas as pd
import altair as alt
from urllib.error import URLError




@st.cache_data
def get_data():
    path_ = "vgsales.csv"
    df = pd.read_csv(path_)
    # drop NAN on Year and Publisher
    df.dropna(inplace= True)
    # cleaning Year column
    df.Year = df.Year.astype('str')
    df.Year = df.Year.str.replace('.0','')
    return df
    

try:
    
    df = get_data()
    
    """ Video games sales analysis """
    # The "#" tells streamlit to read the text as a markdown or a title
    # Another way to do this is to send the text into streamlit .title object as in:
    st.title("A table created by Izunna.")

    
    # total sales metrics
    """ # Sales Metrics"""
    global_sales = np.round(np.sum(df.Global_Sales),2)
    eu_sales = np.round(np.sum(df.EU_Sales),2)
    na_sales = np.round(np.sum(df.NA_Sales),2)
    jp_sales = np.round(np.sum(df.JP_Sales),2)
    other_sales = np.round(np.sum(df.Other_Sales),2)

    # create a ceries of columns
    col1, col2, col3 = st.columns(3)
    col4, col5 = st.columns(2)

    # create card
    col1.metric('Global Sales Total',global_sales,"USD")
    col2.metric('North America Sales',na_sales,"USD")
    col3.metric('European Union Sales',eu_sales,"USD")
    col4.metric('Japan Sales Total',jp_sales,"USD")
    col5.metric('Other Sales',other_sales,"USD")

    st.write("Select a Platform and Genre")

#  Creating filters for platforms columns
    col6, col7 = st.columns(2)
    platforms = df['Platform'].unique() #To send the unique values in the 'Platform cplomn to variable named "platforms"
    selected_platform = col6.multiselect(
        "select from Platform here", platforms,[platforms[0],
                               platforms[1]]
    )
    # Creating filters for genre column
    genre = df.Genre.unique()
    selected_genre = col7.multiselect(
        "Genre", genre,[genre[0], genre[1]]
    )
    filtered_data = df[df['Platform'].isin(selected_platform) &
                       df['Genre'].isin(selected_genre)]

    # table
    if not selected_platform and selected_genre:
        st.error('please select both filters from platform and genre')
    else: 
        st.write('''Filtered result''')
        st.table(filtered_data.head())

        # table end

        # plots
        # bar chart
        st.write(''' ## European Union Sales per Platform ''')
        bar1 = filtered_data.groupby(['Platform'])['EU_Sales'].sum().sort_values(ascending = True)
        st.bar_chart(bar1)
        st.bar_chart(bar1, color = '#d4af37', width=200, height=400)

    st.write("""Filtered result""")
    st.table(filtered_data.head())

    # area chart
    st.write(''' ## European Union Sales over Time ''')
    chart = (
             alt.Chart(filtered_data)
             .mark_line()
             .encode(
                x="Year".format(),
                 y=alt.Y('Global_Sales', stack=None),
                 )
                 )
    st.altair_chart(chart, use_container_width = True)

    # col6(selected_platform)
# countries", list(df.index), ["China", "United States of America"]
#     )
#     if not countries:
#         st.error("Please select at least one country.")
#     else:
#         data = df.loc[countries]
#         data /= 1000000.0
#         st.write("### Gross Agricultural Production ($B)", data.sort_index())

#         data = data.T.reset_index()
#         data = pd.melt(data, id_vars=["index"]).rename(
#             columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
#         )
#         chart = (
#             alt.Chart(data)
#             .mark_area(opacity=0.3)
#             .encode(
#                 x="year:T",
#                 y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
#                 color="Region:N",
#             )
#         )
#         st.altair_chart(chart, use_container_width=True)
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )
 
