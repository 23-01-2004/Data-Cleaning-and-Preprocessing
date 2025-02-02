import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from synthetic_data_generation.data_generation import ComplexMedicalDataGenerator
from src.data_cleaner import MedicalDataCleanerAndVisualizer    # assuming you have the clean_data function in data_cleaner.py

# Title of the app
st.title('Complex Medical Data Generator and Cleaner')

# Sidebar for user input
st.sidebar.header('Settings')
n_records = st.sidebar.number_input('Number of records to generate', min_value=100, max_value=5000, value=1000, step=100)

# Initialize an empty df variable
df = None

# Button to generate dataset
if st.sidebar.button('Generate Dataset'):
    # Create the dataset
    generator = ComplexMedicalDataGenerator(n_records=n_records)
    df = generator.generate_dataset()
    
    # Show the dataset preview
    st.write("### Generated Dataset Preview", df.head())
    st.write("### Dataset Info")
    st.write(df.info())
    
    # Provide an option to download the generated CSV
    csv = df.to_csv(index=False)
    st.download_button("Download Generated Dataset", csv, "generated_data.csv", "text/csv")

    # Display basic charts
    
    # Age Distribution Chart
    if 'Age' in df.columns:
        st.subheader("Age Distribution")
        plt.figure(figsize=(10, 6))
        sns.histplot(df['Age'], kde=True)
        st.pyplot()

    # Gender Distribution Chart
    if 'Gender' in df.columns:
        st.subheader("Gender Distribution")
        plt.figure(figsize=(10, 6))
        sns.countplot(data=df, x='Gender')
        st.pyplot()

# Button to clean data
if st.sidebar.button('Clean Data') and df is not None:
    # Clean the dataset only if it's generated
    df_cleaned = clean_data(df)
    
    # Show cleaned dataset
    st.write("### Cleaned Dataset Preview", df_cleaned.head())
    st.write("### Cleaned Dataset Info")
    st.write(df_cleaned.info())
    
    # Provide an option to download the cleaned CSV
    csv_cleaned = df_cleaned.to_csv(index=False)
    st.download_button("Download Cleaned Dataset", csv_cleaned, "cleaned_data.csv", "text/csv")
    
    # Display charts for cleaned data
    
    # Age Distribution Chart (Cleaned)
    if 'Age' in df_cleaned.columns:
        st.subheader("Cleaned Age Distribution")
        plt.figure(figsize=(10, 6))
        sns.histplot(df_cleaned['Age'], kde=True)
        st.pyplot()

    # Gender Distribution Chart (Cleaned)
    if 'Gender' in df_cleaned.columns:
        st.subheader("Cleaned Gender Distribution")
        plt.figure(figsize=(10, 6))
        sns.countplot(data=df_cleaned, x='Gender')
        st.pyplot()

# Display additional visualizations or custom charts as needed
