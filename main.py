# This is a sample Python script.
import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import os

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

