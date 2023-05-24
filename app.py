import streamlit as st
import pandas as pd
import altair as alt
import openai

# Set page configuration
st.set_page_config(layout="wide")

# OpenAI API authentication
openai.api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

# Create a sidebar with file upload functionality
st.sidebar.title("Upload CSV")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

# Main page content
st.title("Data Visualization and Querying App")
st.write("Upload a CSV file, visualize the data, and ask questions using natural language.")

# Load data if a file has been uploaded
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Display the raw data table
    st.subheader("Raw Data")
    st.write(df)

    # Select a numerical column for the slider
    numeric_columns = df.select_dtypes(include=["int", "float"]).columns.tolist()
    selected_column = st.selectbox("Select a numerical column for the slider", numeric_columns)

    # Create a slider for the selected column
    min_value = float(df[selected_column].min())
    max_value = float(df[selected_column].max())
    default_value = (min_value + max_value) / 2
    slider_value = st.slider("Select a value on the slider", min_value, max_value, default_value)

    # Filter the data based on the slider value
    filtered_df = df[df[selected_column] >= slider_value]

    # Display the filtered data
    st.subheader("Filtered Data")
    st.write(filtered_df)

    # Create a bar chart using Altair
    st.subheader("Bar Chart")
    bar_chart = alt.Chart(filtered_df).mark_bar().encode(
        x=alt.X("count()", title="Count"),
        y=alt.Y(selected_column, title=selected_column)
    )
    st.altair_chart(bar_chart, use_container_width=True)

    # Create a line chart using Altair
    st.subheader("Line Chart")
    line_chart = alt.Chart(filtered_df).mark_line().encode(
        x=alt.X("index", title="Index"),
        y=alt.Y(selected_column, title=selected_column)
    )
    st.altair_chart(line_chart, use_container_width=True)

    # Ask a question using natural language
    question = st.text_input("Ask a question about the data", max_chars=256)
    if question:
        response = openai.Completion.create(
            engine="davinci",
            prompt=f"Question: {question}\nAnswer:",
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        answer = response.choices[0].text.strip()
        st.subheader("Question & Answer")
        st.write(f"Q: {question}")
        st.write(f"A: {answer}")
