import streamlit as st
import pandas as pd
import altair as alt

# Set page configuration
st.set_page_config(layout="wide")

# Create a sidebar with file upload functionality
st.sidebar.title("Upload CSV")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

# Main page content
st.title("Data Visualization with Altair")
st.write("Upload a CSV file and select columns to visualize.")

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
