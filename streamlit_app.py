import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup

# Function to call OpenAI API
def call_openai_api(prompt, document, max_tokens=2000):
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
    max_tokens=max_tokens
  )
  return response['choices'][0]['message']['content']

# Function to scrape a webpage
def scrape_webpage(url, user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"):
  response = requests.get(url, headers={"User-Agent": user_agent})
  soup = BeautifulSoup(response.text, 'html.parser')
  return soup.get_text()

# Streamlit UI
st.title("OpenAI GPT-4 Chatbot")

# Input for OpenAI API Key
api_key = st.text_input("Enter your OpenAI API Key:", type="password")

if api_key:
  openai.api_key = api_key

  # Dropdown for action selection
  action = st.selectbox("Choose an action:", ["Upload a document", "Enter a link to scrape"])

  if action == "Upload a document":
    uploaded_file = st.file_uploader("Upload a document", type=["txt"])
    if uploaded_file:
      document = uploaded_file.read().decode()
      prompt = st.text_input("Enter your prompt:")
      if st.button("Submit"):
        response = call_openai_api(prompt, document, max_tokens=2000)
        st.write(response)
      # Add a Clear button
      st.button("Clear", on_click=lambda: st.session_state["prompt"] = "")

  elif action == "Enter a link to scrape":
    link = st.text_input("Enter the link:")
    prompt = st.text_input("Enter your prompt:")
    if st.button("Scrape and Submit"):
      document = scrape_webpage(link, user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36")
      response = call_openai_api(prompt, document, max_tokens=2000)
      st.write(response)
      # Add a Clear button
      st.button("Clear", on_click=lambda: st.session_state["prompt"] = "")

else:
  st.warning("Please enter your OpenAI API Key to proceed.")
