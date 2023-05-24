import streamlit as st
import pandas as pd
import altair as alt
import openai

# Set up OpenAI API authentication
openai.api_key = ""

# Configure Streamlit app
st.set_page_config(layout="wide")

# Sidebar - OpenAI API key input
st.sidebar.title("OpenAI API Key")
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

# Sidebar - File Upload
st.sidebar.title("Upload CSV")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

# Main page content
st.title("CSV Data Exploration and Question Answering")

# Load data if a file has been uploaded
if uploaded_file is not None:
    # Read CSV file into DataFrame
    df = pd.read_csv(uploaded_file)

    # Display the raw data table
    st.subheader("Raw Data")
    st.write(df)

    # Visualize the data using a scatter plot
    st.subheader("Data Visualization")
    x_axis = st.selectbox("Select X Axis", list(df.columns))
    y_axis = st.selectbox("Select Y Axis", list(df.columns))
    chart = alt.Chart(df).mark_circle().encode(
        x=x_axis,
        y=y_axis,
        tooltip=list(df.columns)
    )
    st.altair_chart(chart, use_container_width=True)

    # User input - question
    question = st.text_input("Ask a question about the data")

    # Answer the question using OpenAI's API
    if st.button("Answer"):
        if api_key:
            openai.api_key = api_key
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
        else:
            st.warning("Please enter your OpenAI API key in the sidebar.")
