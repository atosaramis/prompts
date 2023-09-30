import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup
import pandas as pd
from docx import Document
import pdfplumber

# Function to call OpenAI API
def call_openai_api(prompt, document):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": document
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=2000
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return ""

# Function to scrape a webpage
def scrape_webpage(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return ""

# Streamlit UI
st.title("OpenAI GPT-4 Chatbot")

# Input for OpenAI API Key
api_key = st.text_input("Enter your OpenAI API Key:", type="password")

if api_key:
    openai.api_key = api_key

    # Dropdown for action selection
    action = st.selectbox("Choose an action:", ["Upload a document", "Enter a link to scrape"])

    if action == "Upload a document":
        uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf", "csv", "html", "doc"])
        if uploaded_file:
            if uploaded_file.type == "text/plain":
                document = uploaded_file.read().decode()
            elif uploaded_file.type == "text/csv":
                df = pd.read_csv(uploaded_file)
                document = df.to_string()
            elif uploaded_file.type == "text/html":
                soup = BeautifulSoup(uploaded_file.read().decode(), 'html.parser')
                document = soup.get_text()
            elif uploaded_file.type == "application/pdf":
                with pdfplumber.open(uploaded_file) as pdf:
                    document = "\n".join(page.extract_text() for page in pdf.pages)
            elif uploaded_file.type == "application/msword":
                doc = Document(uploaded_file)
                document = "\n".join(paragraph.text for paragraph in doc.paragraphs)
            else:
                st.warning("Unsupported file type")
                document = ""
            
            prompt = st.text_input("Enter your prompt:")
            if st.button("Submit"):
                response = call_openai_api(prompt, document)
                st.write(response)

    elif action == "Enter a link to scrape":
        link = st.text_input("Enter the link:")
        prompt = st.text_input("Enter your prompt:")
        if st.button("Scrape and Submit"):
            document = scrape_webpage(link)
            response = call_openai_api(prompt, document)
            st.write(response)

else:
    st.warning("Please enter your OpenAI API Key to proceed.")
