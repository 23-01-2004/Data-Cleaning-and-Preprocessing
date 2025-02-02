import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

class MedicalDataCleanerAndVisualizer:
    """
    A class to clean complex, uncleaned medical datasets and generate visualizations.
    """

    def __init__(self, input_file='../data/complex_medical_data.csv', output_file='../cleaned_data/cleaned_data.csv', plot_dir='../cleaned_data_visualization/plots'):
        """
        Initializes the data cleaner and visualizer with the input and output file paths.

        Args:
            input_file (str): The path to the raw dataset (default is '../data/complex_medical_data.csv').
            output_file (str): The path where the cleaned dataset will be saved (default is '../data/cleaned_data.csv').
            plot_dir (str): Directory to save visualizations (default is '../data/plots').
        """
        self.input_file = input_file
        self.output_file = output_file
        self.plot_dir = plot_dir
        if not os.path.exists(self.plot_dir):
            os.makedirs(self.plot_dir)

    def load_data(self):
        """Loads the dataset from the input file."""
        if os.path.exists(self.input_file):
            df = pd.read_csv(self.input_file)
            print("\nData Loaded Successfully")
            return df
        else:
            raise FileNotFoundError(f"File not found: {self.input_file}")

    def clean_patient_id(self, df):
        """Cleans PatientID by ensuring a consistent format."""
        df['PatientID'] = df['PatientID'].apply(lambda x: str(x).strip().upper() if isinstance(x, str) else str(x))
        return df

    def clean_visit_date(self, df):
        """Standardizes VisitDate format to 'YYYY-MM-DD'."""
        df['VisitDate'] = pd.to_datetime(df['VisitDate'], errors='coerce').dt.strftime('%Y-%m-%d')
        return df

    def clean_age(self, df):
        """Cleans Age column by removing impossible values."""
        df['Age'] = df['Age'].apply(lambda x: x if 0 <= x <= 120 else np.nan)
        return df

    def clean_gender(self, df):
        """Standardizes Gender column to 'Male', 'Female', or 'Other'."""
        gender_map = {
            'M': 'Male', 'F': 'Female', 'Male': 'Male', 'Female': 'Female',
            'm': 'Male', 'f': 'Female', 'MALE': 'Male', 'FEMALE': 'Female',
            'Other': 'Other', '': 'Other'
        }
        df['Gender'] = df['Gender'].apply(lambda x: gender_map.get(str(x).strip().upper(), 'Other') if isinstance(x, str) else 'Other')
        return df

    def clean_insurance(self, df):
        """Standardizes Insurance column to remove empty and 'N/A' values."""
        df['Insurance'] = df['Insurance'].apply(lambda x: 'Unknown' if isinstance(x, str) and x in ['N/A', ''] else str(x))
        return df

    def clean_medical_notes(self, df):
        """Removes empty medical notes and standardizes format."""
        df['MedicalNotes'] = df['MedicalNotes'].apply(lambda x: x if isinstance(x, str) and x.strip() != '' else 'No notes available')
        return df

    def clean_temperature(self, df):
        """Standardizes Temperature column to numeric values."""
        df['Temperature'] = df['Temperature'].apply(lambda x: ''.join([i for i in str(x) if i.isdigit() or i == '.']))
        df['Temperature'] = pd.to_numeric(df['Temperature'], errors='coerce')
        return df

    def clean_blood_pressure(self, df):
        """Standardizes BloodPressure column to numeric systolic/diastolic values."""
        def extract_blood_pressure(bp):
            try:
                parts = [int(i) for i in str(bp).replace('/', '-').split() if i.isdigit()]
                if len(parts) == 2:
                    return f"{parts[0]}/{parts[1]}"
                return np.nan
            except:
                return np.nan

        df['BloodPressure'] = df['BloodPressure'].apply(extract_blood_pressure)
        return df

    def handle_missing_values(self, df):
        """Handles missing values by imputing or dropping based on column significance."""
        df['Temperature'] = df['Temperature'].fillna(df['Temperature'].mean())
        df['BloodPressure'] = df['BloodPressure'].fillna('Normal')
        df['MedicalNotes'] = df['MedicalNotes'].fillna('No medical information')
        return df

    def drop_duplicates(self, df):
        """Drops duplicate records."""
        df = df.drop_duplicates(subset=['PatientID', 'VisitDate'])
        return df

    def save_cleaned_data(self, df):
        """Saves the cleaned dataset to the output file."""
        df.to_csv(self.output_file, index=False)
        print(f"\nCleaned data saved to {self.output_file}")

    def plot_data(self, df):
        """Generates visualizations and saves them as images."""
        # Age Distribution
        plt.figure(figsize=(10, 6))
        sns.histplot(df['Age'].dropna(), kde=True, bins=20, color='skyblue')
        plt.title('Age Distribution')
        plt.xlabel('Age')
        plt.ylabel('Frequency')
        plt.savefig(os.path.join(self.plot_dir, 'age_distribution.png'))
        plt.close()

        # Temperature Distribution
        plt.figure(figsize=(10, 6))
        sns.histplot(df['Temperature'].dropna(), kde=True, bins=20, color='lightgreen')
        plt.title('Temperature Distribution')
        plt.xlabel('Temperature')
        plt.ylabel('Frequency')
        plt.savefig(os.path.join(self.plot_dir, 'temperature_distribution.png'))
        plt.close()

        # Blood Pressure Distribution (using systolic and diastolic)
        df['Systolic'] = df['BloodPressure'].apply(lambda x: int(x.split('/')[0]) if isinstance(x, str) and '/' in x else np.nan)
        df['Diastolic'] = df['BloodPressure'].apply(lambda x: int(x.split('/')[1]) if isinstance(x, str) and '/' in x else np.nan)

        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=df['Systolic'], y=df['Diastolic'], color='orange')
        plt.title('Blood Pressure Distribution (Systolic vs Diastolic)')
        plt.xlabel('Systolic')
        plt.ylabel('Diastolic')
        plt.savefig(os.path.join(self.plot_dir, 'blood_pressure_distribution.png'))
        plt.close()

        # Gender Distribution
        plt.figure(figsize=(6, 6))
        sns.countplot(x='Gender', data=df, palette='Set2')
        plt.title('Gender Distribution')
        plt.xlabel('Gender')
        plt.ylabel('Count')
        plt.savefig(os.path.join(self.plot_dir, 'gender_distribution.png'))
        plt.close()

        # Insurance Distribution
        plt.figure(figsize=(6, 6))
        sns.countplot(x='Insurance', data=df, palette='Set3')
        plt.title('Insurance Distribution')
        plt.xlabel('Insurance')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.savefig(os.path.join(self.plot_dir, 'insurance_distribution.png'))
        plt.close()

    def clean_data(self):
        """Performs the data cleaning process."""
        # Load the data
        df = self.load_data()

        # Clean the data step-by-step
        df = self.clean_patient_id(df)
        df = self.clean_visit_date(df)
        df = self.clean_age(df)
        df = self.clean_gender(df)
        df = self.clean_insurance(df)
        df = self.clean_medical_notes(df)
        df = self.clean_temperature(df)
        df = self.clean_blood_pressure(df)

        # Handle missing values and remove duplicates
        df = self.handle_missing_values(df)
        df = self.drop_duplicates(df)

        # Save the cleaned data
        self.save_cleaned_data(df)

        # Plot the data
        self.plot_data(df)

        return df


# Clean the dataset and create visualizations
cleaner = MedicalDataCleanerAndVisualizer(input_file='../data/complex_medical_data.csv', output_file='../cleaned_data/cleaned_data.csv', plot_dir='../cleaned_data_visualization/plots')
cleaned_df = cleaner.clean_data()
