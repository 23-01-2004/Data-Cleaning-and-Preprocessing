# 📊 Data Description

## Overview
This dataset simulates medical records with **various inconsistencies**, **missing values**, and **duplicate entries** to mimic real-world healthcare data. It includes patient details such as age, gender, temperature, medical notes, lab results, and more, with inconsistencies that need to be cleaned and standardized.

---

## Dataset Columns

| **Column Name**   | **Description**                                                                                       |
|-------------------|-------------------------------------------------------------------------------------------------------|
| **PatientID**     | A unique identifier for each patient. Formats vary, e.g., `PXXXX`, `PAT-XXX`, `PATIENT_XXX`, `HXX-XXXX`. |
| **VisitDate**     | The date of the patient's visit in multiple formats (e.g., `YYYY-MM-DD`, `DD/MM/YYYY`, `MM-DD-YYYY`).   |
| **Age**           | The patient's age (can range from -10 to 120). Invalid or negative values are present.                |
| **Gender**        | The patient's gender, which can be inconsistent (e.g., `Male`, `M`, `Female`, `F`, `Other`, or empty).  |
| **Insurance**     | The type of insurance: `Private`, `Medicare`, `Medicaid`, `None`, `N/A`, or empty values.             |
| **MedicalNotes**  | Text notes from the physician about the patient's conditions and symptoms. Some entries may be empty. |
| **Temperature**   | The patient's body temperature in various formats (e.g., `36.5°C`, `98.5°F`, `36.5 C`).               |
| **BloodPressure** | Blood pressure readings in different formats (e.g., `120/80`, `120-80`, `120 over 80`).                |
| **Lab Results**   | Results from various lab tests such as `CBC`, `Glucose`, `Cholesterol`, and `ThyroidTest`. These may contain numeric, categorical, or formatted string values. |

---

## **Data Quality Issues** 🚨

The dataset is designed with real-world issues in mind:

### 1. **Missing Values** 🕳️
   Some fields contain missing data (NaN), intentionally introduced for data cleaning and preprocessing tasks.

### 2. **Inconsistent Formats** 🔄
   The dataset includes inconsistent formats for the following:
   - **Dates** (e.g., `YYYY-MM-DD`, `DD/MM/YYYY`, `MM-DD-YYYY`)
   - **Gender** (e.g., `M`, `Male`, `MALE`, `Other`)
   - **Temperature** (e.g., `36.5°C`, `98.5°F`, `36.5 C`)
   - **Blood Pressure** (e.g., `120/80`, `120-80`, `120 over 80`)
   
   These need to be standardized.

### 3. **Duplicate Records** 🔁
   The dataset includes duplicates that must be identified and removed during the cleaning process.

---

## Visual Representations 🖼️

After cleaning the dataset, visualizations will help explore the following:

1. **Age Distribution**: The age range and distribution of patients.
2. **Temperature Distribution**: The spread of body temperatures.
3. **Blood Pressure Distribution**: The relationship between systolic and diastolic readings.
4. **Gender Distribution**: A breakdown of the genders in the dataset.
5. **Insurance Type Distribution**: How the insurance types are distributed among the patients.

---

## Conclusion
This dataset provides a challenging yet realistic environment for **data cleaning** and **preprocessing** tasks, simulating typical issues that arise when working with medical records. It is ideal for testing and improving your skills in handling unstructured, messy healthcare data.
