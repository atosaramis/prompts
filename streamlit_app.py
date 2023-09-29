import streamlit as st
import openai

# Function to call OpenAI API
def call_openai_api(prompt):
    response = openai.Completion.create(engine="davinci", prompt=prompt, max_tokens=150)
    return response.choices[0].text.strip()

# Streamlit UI
st.title("OpenAI GPT-4 Chatbot")

# Input for OpenAI API Key
api_key = st.text_input("Enter your OpenAI API Key:", type="password")

if api_key:
    openai.api_key = api_key

    # Dropdown for action selection
    action = st.selectbox("Choose an action:", ["Enter a prompt", "Upload a document", "Enter a link to scrape"])

    if action == "Enter a prompt":
        prompt = st.text_area("Enter your prompt:")
        if st.button("Submit"):
            response = call_openai_api(prompt)
            st.write(response)

    elif action == "Upload a document":
        uploaded_file = st.file_uploader("Upload a document", type=["txt"])
        if uploaded_file:
            document = uploaded_file.read().decode()
            response = call_openai_api(document)
            st.write(response)

    elif action == "Enter a link to scrape":
        # Note: Actual scraping requires additional libraries and handling. This is a basic example.
        link = st.text_input("Enter the link:")
        if st.button("Scrape and Submit"):
            # Here, you'd typically scrape the content from the link and then pass it to the API.
            # For simplicity, we're just passing the link as a prompt.
            response = call_openai_api(link)
            st.write(response)

else:
    st.warning("Please enter your OpenAI API Key to proceed.")
