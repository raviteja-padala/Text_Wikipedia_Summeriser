import requests
from bs4 import BeautifulSoup as bs
import streamlit as st
from txtai.pipeline import Summary

st.set_page_config(layout="wide")

@st.cache_resource
def text_summary(text, maxlength=None):
    # Create a summary instance
    summary = Summary()
    result = summary(text)
    return result

def scrape_wiki(search_string):
    website = "https://en.wikipedia.org/wiki/"
    url = website + search_string

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Parse the HTML content with BeautifulSoup
    soup = bs(response.content, 'html.parser')

    # Find the <div> element with the specified class
    content_div = soup.find('div', {'class': "mw-body-content mw-content-ltr"})

    # Extract the text content from the <div> element
    if content_div:
        extracted_text = content_div.get_text()

    # Limit the extracted text to a maximum of 1000 words
    words = extracted_text.split()
    if len(words) > 2000:
        extracted_text = ' '.join(words[:2000])

    return extracted_text

choice = st.sidebar.selectbox("Select your choice", ["Summarize Text", "Summarize Wiki"])

if choice == "Summarize Text":
    st.subheader("Summarize Text using txtai")
    input_text = st.text_area("Enter your text here")
    if st.button("Summarize Text"):
        st.markdown("**Summary Result**")
        result = text_summary(input_text)
        st.success(result)
        st.markdown("**Your Input Text**")
        st.info(input_text)
elif choice == "Summarize Wiki":
    st.subheader("Summarize Wikipedia Article")
    search_string = st.text_input("Enter the search string for Wikipedia")
    if st.button("Search Wikipedia"):
        extracted_text = scrape_wiki(search_string)
        st.markdown("**Summary of Wiki Text**")
        result = text_summary(extracted_text)
        st.success(result)
        st.markdown("**Extracted Wiki Text**")
        st.info(extracted_text)
