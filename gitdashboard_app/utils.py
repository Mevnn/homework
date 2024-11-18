"Contains the functions used by app.py to run the streamlit app"
import collections
import re

import requests
import streamlit as st


def fetch_data(url):
    "Fetch data from the endpoint from the url parameter"
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        return response
    st.write(f"Error, the API returned the following error: {response.status_code}")
    st.stop()


def find_most_common_word(text):
    """Split the words, put in lowercase and remove punctuation"""
    words = re.findall(r"\b\w+\b", text.lower())
    if not words:  # Check if the list is empty
        return "", 0  # Return an empty string and count of
    word_counts = collections.Counter(words)
    most_common_word, most_common_count = word_counts.most_common(1)[0]
    return most_common_word, most_common_count
