# This is a sample Python script.
import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import os

incidents = pd.read_csv(
    "data/Incidents/LFB Incident data from 2009 - 2017.csv",
    low_memory=False
)

print(incidents.head())