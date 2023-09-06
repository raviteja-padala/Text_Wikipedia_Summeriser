import re
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

    # Initialize a list to store the extracted text
    extracted_text_list = []

    # Extract the text content from the <div> element
    if content_div:
        for paragraph in content_div.find_all('p'):
            # Replace hyperlinks with spaces
            paragraph_text = re.sub(r'\[.*?\]', ' ', ' '.join(paragraph.stripped_strings))
            extracted_text_list.append(paragraph_text)

    # Join the extracted paragraphs into a single text
    extracted_text = ' '.join(extracted_text_list)

    # Limit the extracted text to a maximum of 5000 words
    words = extracted_text.split()
    if len(words) > 3000:
        extracted_text = ' '.join(words[:3000])

    return extracted_text

st.title('Text :book: / Wikipedia :computer: Summeriser :memo:')
choice = st.sidebar.selectbox("Select your choice", ["Summarize Text", "Summarize Wiki"])

if choice == "Summarize Text":
    st.subheader("Summarize your Text :book:")
    input_text = st.text_area("Enter your text here")
    if st.button("Summarize Text"):
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("**Your Input Text**")
            st.info(input_text)
        with col2:
            st.markdown("**Summary Result**")
            result = text_summary(input_text)
            st.success(result)
elif choice == "Summarize Wiki":
    st.subheader("Summarize Wikipedia Article :computer:")
    search_string = st.text_input("Enter the search string for Wikipedia")
    if st.button("Search Wikipedia"):
        extracted_text = scrape_wiki(search_string)
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("**Extracted Wiki Text**")
            with st.container():
                st.info(extracted_text)
        with col2:
            st.markdown("**Summary of Wiki Text**")
            result = text_summary(extracted_text)
            st.success(result)
