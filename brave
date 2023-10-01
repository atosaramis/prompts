# app.py

import streamlit as st
import requests
import datetime

BRAVE_API_ENDPOINT = "https://api.search.brave.com/news"
API_KEY = "YOUR_BRAVE_API_KEY"

@st.cache
def brave_search(query, page=1):
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "api.search.brave.com"
    }
    params = {"q": query, "page": page}
    response = requests.get(BRAVE_API_ENDPOINT, headers=headers, params=params)
    return response.json()

st.title("Brave Search Interface")

# Search Bar
search_query = st.text_input("Enter your search query:")

# Filters
date_filter = st.date_input("Filter by Date", datetime.date.today())
sort_order = st.selectbox("Sort By", ["Relevance", "Date"])

# Search Button
if st.button("Search"):
    results = brave_search(search_query)
    if 'data' in results:
        for article in results['data']:
            st.subheader(article['title'])
            st.write(article['description'])
            st.write(article['url'])
            st.write("---")
    else:
        st.error("Error fetching results. Please try again.")

# Pagination
page = st.slider("Page", 1, 10)
if page > 1:
    results = brave_search(search_query, page)
    for article in results['data']:
        st.subheader(article['title'])
        st.write(article['description'])
        st.write(article['url'])
        st.write("---")

# Error Handling
try:
    results = brave_search(search_query)
except requests.exceptions.RequestException as e:
    st.error(f"API Error: {e}")

# API Key Management
api_key_input = st.text_input("Enter your API key:", type="password")
if api_key_input:
    API_KEY = api_key_input

# Theming & Styling (You can expand on this with custom CSS and more)
st.markdown("""
<style>
    body {
        background-color: #f4f4f4;
    }
</style>
""", unsafe_allow_html=True)
