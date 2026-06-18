import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import os

# 1. Import Data

# LOAD INCIDENT DATA

incident_files = [
    "data/Incidents/LFB Incident data from 2018 - 2023.xlsx",
    "data/Incidents/LFB Incident data from 2009 - 2017.csv"
]

incident_dfs = []

for file in incident_files:
    if file.endswith(".csv"):
        df = pd.read_csv(file, low_memory=False)
    else:
        df = pd.read_excel(file)

    incident_dfs.append(df)

incidents = pd.concat(incident_dfs, ignore_index=True)

print("Incidents shape:", incidents.shape)
print(incidents.head())

# LOAD MOBILISATION DATA

mobilisation_files = [
    "data/Mobilisation/LFB Mobilisation data from 2015 - 2020.xlsx",
    "data/Mobilisation/LFB Mobilisation data from 2021 - 2024.csv"
]

mobilisation_dfs = []

for file in mobilisation_files:
    if file.endswith(".csv"):
        df = pd.read_csv(file, low_memory=False)
    else:
        df = pd.read_excel(file)

    mobilisation_dfs.append(df)

mobilisation = pd.concat(mobilisation_dfs, ignore_index=True)

print("Mobilisation shape:", mobilisation.shape)
print(mobilisation.head())

# 2. Summary Tables

# 2.1 Incidents

# Creating summary table:

# Making sure pandas doesn't wrap columns:
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', 1000)       # Set display width

summary = pd.DataFrame({
    "Column Name": incidents.columns,
    "Data Type": incidents.dtypes.values,
    "Missing Values": incidents.isnull().sum().values,
    "Missing %": incidents.isnull().mean().values * 100,
    "Unique Values": incidents.nunique().values
})

print(summary)

# 2.2 Mobilisation

# Creating summary table:

# Making sure pandas doesn't wrap columns:
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', 1000)       # Set display width

summary = pd.DataFrame({
    "Column Name": mobilisation.columns,
    "Data Type": mobilisation.dtypes.values,
    "Missing Values": mobilisation.isnull().sum().values,
    "Missing %": mobilisation.isnull().mean().values * 100,
    "Unique Values": mobilisation.nunique().values
})

print(summary)

# 3. Pre-Prep for Joining Data
# 3.1 Incident Records

# filter only years from 2015 to 2023
incidents = incidents.loc[(incidents["CalYear"] >= 2015) & (incidents["CalYear"] <= 2023)]

# show column names
incidents.columns

# Drop redundant columns
incidents = incidents.drop([
    "TimeOfCall",
    "SpecialServiceType",
    "AddressQualifier",
    "Postcode_full",
    "UPRN",
    "USRN",
    "IncGeo_BoroughCode",
    "ProperCase",
    "IncGeo_WardName",
    "IncGeo_WardCode",
    "Easting_m",
    "Northing_m",
    "Latitude",
    "Longitude",
    "FRS",
    "NumStationsWithPumpsAttending",
    "NumPumpsAttending",
    "SecondPumpArriving_AttendanceTime",
    "SecondPumpArriving_DeployedFromStation",

], axis=1)

# display shape
incidents.shape

# Save dataset
incidents.to_csv(
    "data/Incidents/incidents_2015_2023.csv",
    index=False
)

# 3.2 Mobilization Records

# filter only years between 2015 and 2023
mobilisation = mobilisation.loc[(mobilisation["CalYear"] >= 2015) & (mobilisation["CalYear"] <= 2023)]

# filter only first pump
mobilisation = mobilisation.sort_values(
    ["IncidentNumber", "PumpOrder"]
).drop_duplicates("IncidentNumber")

# drop redundant columns
mobilisation = mobilisation.drop([
    "Resource_Code",
    "AttendanceTimeSeconds",
    "DateAndTimeLeft",
    "DateAndTimeReturned",
    "DeployedFromStation_Code",
    "PlusCode_Code",
    "BoroughName",
    "WardName"
], axis=1)

# display shape
mobilisation.shape

# Save dataset
mobilisation.to_csv(
    "data/Mobilisation/mobilisation_2015_2023.csv",
    index=False
)

# 4. Joining Datasets

# merge incidents and mobilisation (pump order == 1)
df_merged = incidents.merge(mobilisation, on="IncidentNumber", how = "left")

df_merged.shape

# double check for duplicates
df_merged["IncidentNumber"].duplicated().sum()

# save data set
df_merged.to_csv(
    "data/df_merged_2015_2023.csv",
    index=False
)

# Importing basic Python libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import os

# Load dataset
df = pd.read_csv("data/df_merged_2015_2023.csv", low_memory=False)

# Display shape
print(df.shape)

# Preview data
df.head()

# Making sure pandas doesn't wrap columns:
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', 1000)       # Set display width
df.head()

# create summary table

# define parameters for summary table
summary = pd.DataFrame({
    "Column Name": df.columns,
    "Data Type": df.dtypes.values,
    "Missing values": df.isna().sum().values,
    "Missing values in %": (df.isnull().sum().values) / len(df) * 100,
    "Unique values": df.nunique().values
})

# display number of rows and columns
rows, cols = df.shape

# display summary table
print("-------------------------")
print("Summary table:")
print("-------------------------\n")

print("Number of rows:", rows)
print("Number of columns:", cols)
print("\n-------------------------\n")
print(summary)

# Pre-Cleaning

# display columns to identify redundant columns
df.columns

# delete all redundant columns after merging
cols_to_drop = [
    "source_file_x", "source_file_y", # columns were created while loading full data for better debugging but are now redundant
    'CalYear_y', 'HourOfCall_y',      # dupliactes of second dataset
]

df = df.drop(columns=cols_to_drop, errors="ignore")

# display shape
df.shape

# Filter Boroughs

df = df.loc[(df["IncGeo_BoroughName"] == "WESTMINSTER") | (df["IncGeo_BoroughName"] == "HAVERING")]


