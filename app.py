import streamlit as st

from helper import preprocessing_data, graph_sentiment, analyse_mention, analyse_hastag, download_data

st.set_page_config(
     page_title="Brand Reputation Finder",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
)


st.title("Brand Reputation Finder")

function_option = st.sidebar.selectbox("Select The Funtionality: ", ["Search By #Tag and Words", "Search By Username"])
if function_option == "Search By #Tag and Words":
    word_query = st.text_input("Enter the Hastag or any word")
elif function_option == "Search By Username":
    word_query = st.text_input("Enter the Username ( Don't include @ )")

number_of_tweets = st.slider("Number of tweets to be pulled regarding the query: {}".format(word_query), min_value=100, max_value=100 ** 2)
st.info(f"100 Tweets take approximately 5 sec. "
        f"So you might have to wait {round((number_of_tweets*0.05/60),2)} minute(s) for {number_of_tweets} Tweets")

if st.button("Collect and Analyze Tweets"):
    data = preprocessing_data(word_query, number_of_tweets, function_option)
    analyse = graph_sentiment(data)
    mention = analyse_mention(data)
    hastag = analyse_hastag(data)

    st.write(" \n ")
    st.header("Preprocessed Tweets")
    st.write(data)
    download_data(data, label=f"tweets_{word_query.replace(' ', '_')}")
    st.write(" ")
    
    # EDA
    _, eda_col, _ = st.columns(3)
    with eda_col:
        st.markdown("### EDA On the Data")

    #
    col1, col2 = st.columns(2)
    with col1:
        st.text("Users with most @mentions in the {} tweets".format(number_of_tweets))
        st.bar_chart(mention)
    with col2:
        st.text("Most used #hashtags in the {} tweets".format(number_of_tweets))
        st.bar_chart(hastag)
    
    col3, col4 = st.columns(2)
    with col3:
        st.text("Most referred/linked websites in the {} tweets".format(number_of_tweets))
        st.bar_chart(data["links"].value_counts().head(10).reset_index())
    with col4:
        st.text("List of tweets linking to most referred websites")
        filtered_data = data[data["links"].isin(data["links"].value_counts().head(10).reset_index()["index"].values)]
        st.write(filtered_data)

    st.subheader(f"Brand Reputation Breakdown - `{word_query}`")
    st.bar_chart(analyse)
    