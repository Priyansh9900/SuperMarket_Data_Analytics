import streamlit as st
import pandas as pd
import plotly.express as px

# Function to load CSV
def load_csv(file):
    return pd.read_csv(file)

# Function to display dataframe
def display_dataframe(df):
    st.write(df)

# Function to filter dataframe
def filter_dataframe(df):
    if st.checkbox("Filter Data"):
        columns = df.columns.tolist()
        column_to_filter = st.selectbox("Select Column to Filter", columns)
        unique_values = df[column_to_filter].unique()
        filter_value = st.selectbox("Select Value", unique_values)
        filtered_df = df[df[column_to_filter] == filter_value]
        return filtered_df
    return df

# Function to create plots
def create_plots(df):
    st.sidebar.header("Create Plot")
    plot_type = st.sidebar.selectbox("Select Plot Type", ["Scatter Plot", "Line Plot", "Bar Plot"])
    
    columns = df.columns.tolist()
    x_axis = st.sidebar.selectbox("Select X-axis", columns)
    y_axis = st.sidebar.selectbox("Select Y-axis", columns)
    
    additional_params = {}
    
    if plot_type == "Scatter Plot":
        color = st.sidebar.selectbox("Select Color Column (optional)", [None] + columns)
        size = st.sidebar.selectbox("Select Size Column (optional)", [None] + columns)
        
        if color:
            additional_params['color'] = color
        if size:
            additional_params['size'] = size
        
        fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{plot_type} of {x_axis} vs {y_axis}", **additional_params)
    elif plot_type == "Line Plot":
        fig = px.line(df, x=x_axis, y=y_axis, title=f"{plot_type} of {x_axis} vs {y_axis}")
    elif plot_type == "Bar Plot":
        fig = px.bar(df, x=x_axis, y=y_axis, title=f"{plot_type} of {x_axis} vs {y_axis}")
    
    st.plotly_chart(fig)

# Main Streamlit app
def main():
    st.title("Interactive Data Dashboard")
    
    st.sidebar.header("Upload CSV")
    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        df = load_csv(uploaded_file)
        st.sidebar.write("File Uploaded Successfully!")
        
        st.header("Data Preview")
        display_dataframe(df)
        
        st.header("Filter Data")
        filtered_df = filter_dataframe(df)
        display_dataframe(filtered_df)
        
        st.header("Summary Statistics")
        st.write(filtered_df.describe())
        
        st.header("Create Interactive Plots")
        create_plots(filtered_df)

if __name__ == "__main__":
    main()
