import streamlit as st
import pandas as pd
import altair as alt
import openai

# Set page configuration
st.set_page_config(layout="wide")

# Create a sidebar with file upload functionality and OpenAI API key input
st.sidebar.title("Upload CSV")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

st.sidebar.title("OpenAI Settings")
openai_api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

# Configure OpenAI API
openai.api_key = openai_api_key

# Main page content
st.title("Data Visualization and Question Answering with Altair and OpenAI")
st.write("Upload a CSV file and select columns to visualize. Ask questions about the data using OpenAI.")

# Load data if a file has been uploaded
if uploaded_file is not None:
df = pd.read_csv(uploaded_file)

# Display the raw data table
st.subheader("Raw Data")
st.write(df)

# Allow the user to select columns for visualization
columns = list(df.columns)
x_axis = st.sidebar.selectbox("Select X Axis", columns)
y_axis = st.sidebar.selectbox("Select Y Axis", columns)

# Create a chart using Altair
chart = alt.Chart(df).mark_bar().encode(
x=x_axis,
y=y_axis
).properties(
width=700,
height=500
)

# Display the chart
st.subheader("Data Visualization")
st.altair_chart(chart, use_container_width=True)

# Allow the user to ask questions using OpenAI
question = st.text_input("Ask a question about the data")

if st.button("Ask"):
if openai_api_key:
response = openai.Completion.create(
engine="text-davinci-002",
prompt=question,
max_tokens=100,
n=1,
stop=None,
temperature=0.5,
)

answer = response.choices[0].text.strip()
st.subheader("Answer")
st.write(answer)
else:
st.warning("Please enter your OpenAI API key in the sidebar.")
