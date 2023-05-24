import streamlit as st
import pandas as pd
import openai

# Set up OpenAI API authentication
openai.api_key = "YOUR_OPENAI_API_KEY"

# Configure Streamlit app
st.set_page_config(layout="wide")

# Sidebar - File Upload
st.sidebar.title("Upload CSV")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

# Main page content
st.title("CSV Data Exploration with Natural Language")

# Load data if a file has been uploaded
if uploaded_file is not None:
    # Read CSV file into DataFrame
    df = pd.read_csv(uploaded_file)

    # Display the raw data table
    st.subheader("Raw Data")
    st.write(df)

    # User input - question
    question = st.text_input("Ask a question about the data")

    # Answer the question using OpenAI's API
    if st.button("Answer"):
        response = openai.Completion.create(
            engine="davinci-codex",
            prompt=f"Question: {question}\nData: {df.to_string()}",
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.3
        )
        answer = response.choices[0].text.strip()
        st.subheader("Answer:")
        st.write(answer)
