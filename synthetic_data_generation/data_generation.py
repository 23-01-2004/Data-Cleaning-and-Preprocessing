import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

class ComplexMedicalDataGenerator:
    """
    A class to generate a complex, uncleaned medical dataset for data cleaning and preprocessing tasks.
    This dataset includes missing values, inconsistent formats, and duplicate entries to simulate real-world medical data.

    Attributes:
        n_records (int): Number of records to generate.
        output_dir (str): Directory path where the dataset will be saved.
    """

    def __init__(self, n_records=1000, output_dir='../data'):
        """
        Initializes the data generator with specified number of records and output directory.

        Args:
            n_records (int): The number of patient records to generate. Default is 1000.
            output_dir (str): The directory where the dataset will be saved. Default is '../data'.
        """
        self.n_records = n_records
        self.output_dir = output_dir
        np.random.seed(42)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_patient_id(self):
        """Generates random patient IDs in various formats to simulate data inconsistency."""
        formats = [
            lambda: f"P{str(random.randint(0, 9999)).zfill(4)}",
            lambda: f"PAT-{random.randint(0, 999)}",
            lambda: f"PATIENT_{random.randint(0, 999)}",
            lambda: f"H{random.randint(0, 99)}-{random.randint(0, 9999)}"
        ]
        return random.choice(formats)()

    def generate_complex_date(self):
        """Generates dates in various formats to introduce inconsistencies."""
        formats = [
            lambda d: d.strftime('%Y-%m-%d'),
            lambda d: d.strftime('%d/%m/%Y'),
            lambda d: d.strftime('%m-%d-%Y'),
            lambda d: d.strftime('%Y/%m/%d'),
            lambda d: d.strftime('%d-%b-%Y'),
            lambda d: d.strftime('%B %d, %Y')
        ]
        base_date = datetime(2020, 1, 1)
        days = random.randint(-1000, 500)
        date = base_date + timedelta(days=days)
        return random.choice(formats)(date)

    def generate_complex_vitals(self):
        """Generates vital signs (temperature and blood pressure) in various formats."""
        temp_formats = [
            lambda t: f"{t:.1f}°C",
            lambda t: f"{(t * 9/5) + 32:.1f}°F",
            lambda t: f"{t:.1f}",
            lambda t: f"{t:.1f} C",
            lambda t: f"{(t * 9/5) + 32:.1f} F"
        ]
        bp_formats = [
            lambda s, d: f"{s}/{d}",
            lambda s, d: f"{s}-{d}",
            lambda s, d: f"{s}\\{d}",
            lambda s, d: f"{s} over {d}",
            lambda s, d: f"{s}"  # Incomplete reading
        ]
        temp = random.uniform(35.5, 40.5)
        sys = random.randint(90, 180)
        dia = random.randint(60, 100)
        return {
            'Temperature': random.choice(temp_formats)(temp),
            'BloodPressure': random.choice(bp_formats)(sys, dia)
        }

    def generate_lab_results(self):
        """Generates lab results with mixed data types (numeric, categorical, and formatted strings)."""
        result_types = [
            lambda: random.uniform(0, 10),
            lambda: f"{random.uniform(0, 10):.2f}",
            lambda: random.choice(['Positive', 'Negative', 'Inconclusive']),
            lambda: f"{random.randint(0, 100)}%",
            lambda: f"< {random.uniform(0, 5):.1f}",
            lambda: f"> {random.uniform(5, 10):.1f}"
        ]
        return random.choice(result_types)()

    def generate_medical_notes(self):
        """Generates random medical notes with varying completeness and formats."""
        conditions = ['Hypertension', 'Diabetes', 'Asthma', 'COPD', 'Arthritis']
        symptoms = ['fever', 'cough', 'fatigue', 'pain', 'nausea']
        medications = ['Aspirin', 'Lisinopril', 'Metformin', 'Ventolin']
        note_formats = [
            lambda: f"Patient presents with {random.choice(symptoms)}. Diagnosed with {random.choice(conditions)}.",
            lambda: f"Prescribed {random.choice(medications)} for {random.choice(conditions)}",
            lambda: f"{random.choice(conditions).upper()} - {random.choice(symptoms)} observed",
            lambda: f"History of {random.choice(conditions)}; new symptoms: {random.choice(symptoms)}",
            lambda: ""  # Empty notes
        ]
        return random.choice(note_formats)()

    def generate_dataset(self):
        """
        Generates the complete dataset, introducing missing values, inconsistent formats, and duplicate entries.

        Returns:
            pd.DataFrame: The generated medical dataset.
        """
        data = {
            'PatientID': [self.generate_patient_id() for _ in range(self.n_records)],
            'VisitDate': [self.generate_complex_date() for _ in range(self.n_records)],
            'Age': np.random.randint(-10, 120, size=self.n_records),
            'Gender': np.random.choice(['M', 'F', 'Male', 'Female', 'm', 'f', 'MALE', 'FEMALE', 'Other', ''], size=self.n_records),
            'Insurance': np.random.choice(['Private', 'Medicare', 'Medicaid', 'None', '', 'N/A'], size=self.n_records),
            'MedicalNotes': [self.generate_medical_notes() for _ in range(self.n_records)]
        }

        vitals = [self.generate_complex_vitals() for _ in range(self.n_records)]
        data['Temperature'] = [v['Temperature'] for v in vitals]
        data['BloodPressure'] = [v['BloodPressure'] for v in vitals]

        for test in ['CBC', 'Glucose', 'Cholesterol', 'ThyroidTest']:
            data[f'{test}_Result'] = [self.generate_lab_results() for _ in range(self.n_records)]

        df = pd.DataFrame(data)
        missing_mask = np.random.choice([True, False], size=df.shape, p=[0.1, 0.9])
        df[missing_mask] = np.nan

        duplicates = df.sample(n=50)
        duplicates['VisitDate'] = duplicates['VisitDate'].apply(lambda x: self.generate_complex_date())
        df = pd.concat([df, duplicates]).sample(frac=1).reset_index(drop=True)

        output_path = os.path.join(self.output_dir, 'complex_medical_data.csv')
        df.to_csv(output_path, index=False)

        print("\nDataset Preview:")
        print(df.head())
        print("\nDataset Info:")
        print(df.info())
        print("\nMissing Values Summary:")
        print(df.isnull().sum())

        return df

# Generate and save dataset
generator = ComplexMedicalDataGenerator(n_records=1000)
df = generator.generate_dataset()
