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

# Modalities

# modalities of columns where number of unique values are less than 20

for col in df.columns:
  if len(df[col].unique()) < 20:
        print(f"Modalities of {col}:\n{df[col].unique()}\n")

# Outliers

# detect implausible values regarding response time
# drop missing values since they haven´t been replaced yet
no_nans = df.dropna(subset=["FirstPumpArriving_AttendanceTime"])

# create boxplot with seaborn
plt.figure()
sns.boxplot(x=no_nans["FirstPumpArriving_AttendanceTime"])
plt.title("Boxplot of First Pump Attendance Time")
plt.xlabel("Attendance Time in seconds")
plt.show()

# Missing Values & Duplicates

# calculate sum of missing values
missing = df.isna().sum()

# percentage of missing values
missing_pct = df.isna().mean() * 100

# combine into one table
missing_summary = pd.DataFrame({
    "Missing Values": missing,
    "Missing Percentage (%)": missing_pct
})

# keep only columns with missing values
missing_summary = missing_summary[missing_summary["Missing Values"] > 0]

print(missing_summary)

# Visualize NaNs
# display bar plot to visualize missing values

plt.figure(figsize=(10,6))
df.isnull().sum().plot(kind="bar")

# Detect Duplicates
# Number of duplicates
print("Number of duplicates:", df.duplicated().sum())

df.columns

# Modification
# Fill NaNs

# Replace "NULL" with 0 in DelayCodeId column
df.loc[:, "DelayCodeId"] = df["DelayCodeId"].fillna(0)

# Replace "NULL" with 'No Delay' in DelayCode_Description column
df.loc[:, "DelayCode_Description"] = df["DelayCode_Description"].fillna("No Delay")

# "DelayCodeId" column should be an integer:
df.loc[:,"DelayCodeId"] = df["DelayCodeId"].fillna(0).astype("Int64")

# Final overview after data conversion:
df.info()

# drop rows altough NaNs > 0.05% but it is the target variable.
# Imputing would create artifical values and therefore would distort analysis

df = df.dropna(subset=["FirstPumpArriving_AttendanceTime"])

# Data Type

# Convert Date and Time columns from object to dateime format

date_cols = [
    "DateOfCall",
    "DateAndTimeMobilised",
    "DateAndTimeMobile",
    "DateAndTimeArrived"
]

for col in date_cols:
    df[col] = pd.to_datetime(
        df[col],
        format="mixed",
        errors="coerce",
        dayfirst=True
    )

# select all columns with data type object
object_cols = df.select_dtypes(include=["object"]).columns

# convert to string
df[object_cols] = df[object_cols].astype("string")

# Column NumCalls: convert from float to integer
df["NumCalls"] = df["NumCalls"].astype("Int64")

# Rename Columns

# show column names
df.columns

# rename columns for better readability / understanding

df = df.rename(columns={
    "CalYear_x" : "Year",
    "HourOfCall_x" : "HourOfCall",
    "IncGeo_BoroughName" : "BoroughName",
    "IncGeo_WardNameNew" : "WardName"
})

# Final Summary Table

# create summary table
summary = pd.DataFrame({
    "Column Name": df.columns,
    "Data Type": df.dtypes.values,
    "Missing Values": df.isna().sum().values,
    "Missing (%)": (df.isna().sum().values / len(df) * 100).round(2),
    "Unique Values": df.nunique().values
})

# sort by missing values
summary = summary.sort_values(by="Missing (%)", ascending=False)

# reset index
summary = summary.reset_index(drop=True)

# display dataset shape
rows, cols = df.shape
print(f"Dataset Shape: {rows} rows × {cols} columns\n")

# display table nicely
print(summary)

# Save Data
df.to_csv(
    r"D:\PycharmProjects\Project-London-Fire-Brigade\data\df_Final_NEW.csv",
    index=False
)

# Visualization
# Preparation

# add column for mobilisation is true or false
df["HasMobilisation"] = df["ResourceMobilisationId"].notna()
df["HasMobilisation"].value_counts()

# filter only rows where HasMobilisation euqals True and create copy for further processing
df_has_mobilisation = df.loc[(df["HasMobilisation"] == True)].copy()

# create column to indicate whethere the 6 min service level agreement was met or not
df_has_mobilisation["Met_6min"] = (df["FirstPumpArriving_AttendanceTime"] <= 360).astype(int)

df_has_mobilisation.to_csv(r"D:\PycharmProjects\Project-London-Fire-Brigade\data\df_has_mobilisation.csv",
    index=False
)

# create column for weekday for temporal analysis
df_has_mobilisation["Weekday"] = df_has_mobilisation["DateOfCall"].dt.day_name()
# ordered weekday
weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Distribution Target Variable
# create histogram
sns.histplot(no_nans["FirstPumpArriving_AttendanceTime"], bins=50)
plt.show()

# Compliance Rate Westminster vs. Havering
# Calculate compliance rate (percentage of incidents within 6 minutes)
compliance = (
    df_has_mobilisation
    .groupby("BoroughName")["Met_6min"]  # group by borough
    .mean()                              # compute share of incidents meeting target
    .sort_values(ascending=False)        # sort from best to worst
    * 100                                # convert to percentage
)

# Create bar chart
plt.figure(figsize=(8, 5))
plt.bar(compliance.index, compliance.values)

# Add titles and labels
plt.title("Compliance with 6-Minute Standard by Borough")
plt.xlabel("Borough")
plt.ylabel("Compliance Rate (%)")
plt.ylim(0, 100)

# Add percentage labels on top of each bar
for i, v in enumerate(compliance.values):
    plt.text(i, v + 1, f"{v:.1f}%", ha="center")

# Improve layout and display plot
plt.tight_layout()
plt.show()

# Response Time by Borough
# Extract response time data for each borough
westminster = df_has_mobilisation[
    df_has_mobilisation["BoroughName"] == "WESTMINSTER"
]["FirstPumpArriving_AttendanceTime"].dropna()

havering = df_has_mobilisation[
    df_has_mobilisation["BoroughName"] == "HAVERING"
]["FirstPumpArriving_AttendanceTime"].dropna()

# Create boxplot comparing both boroughs
plt.figure(figsize=(8, 5))
plt.boxplot(
    [westminster, havering],               # data for both groups
    tick_labels=["Westminster", "Havering"]  # x-axis labels
)

# Add title and axis label
plt.title("Boxplot of Attendance Time by Borough")
plt.ylabel("Attendance Time (seconds)")

# Adjust layout and display plot
plt.tight_layout()
plt.show()

#Distribution of Response Time
# Create a figure with a defined size (width=10, height=5)
plt.figure(figsize=(10, 5))

# Filter response time data for Westminster and remove missing values
westminster = df_has_mobilisation[
    df_has_mobilisation["BoroughName"] == "WESTMINSTER"
]["FirstPumpArriving_AttendanceTime"].dropna()

# Filter response time data for Havering and remove missing values
havering = df_has_mobilisation[
    df_has_mobilisation["BoroughName"] == "HAVERING"
]["FirstPumpArriving_AttendanceTime"].dropna()

# Plot histogram for Westminster
# bins=50 controls the resolution of the histogram
# alpha=0.5 makes the bars semi-transparent so both distributions are visible
plt.hist(westminster, bins=50, alpha=0.5, label="Westminster")

# Plot histogram for Havering (overlaid with Westminster)
plt.hist(havering, bins=50, alpha=0.5, label="Havering")

# Add title and axis labels for clarity
plt.title("Distribution of First Pump Attendance Time")
plt.xlabel("Attendance Time (seconds)")
plt.ylabel("Frequency")

# Add legend to distinguish between the two boroughs
plt.legend()

# Adjust layout to prevent overlapping labels
plt.tight_layout()

# Display the plot
plt.show()

# Days-of-Week Analysis

weekday_compliance = (
    df_has_mobilisation.groupby(["Weekday", "BoroughName"])["Met_6min"]
    .mean()
    .reset_index()
)

weekday_compliance["Weekday"] = pd.Categorical(
    weekday_compliance["Weekday"],
    categories=weekday_order,
    ordered=True
)

weekday_compliance = weekday_compliance.sort_values("Weekday")

plt.figure(figsize=(10, 5))

for borough in ["WESTMINSTER", "HAVERING"]:
    subset = weekday_compliance[weekday_compliance["BoroughName"] == borough]
    plt.plot(subset["Weekday"], subset["Met_6min"] * 100, marker="o", label=borough)

plt.title("Compliance Rate by Day of Week")
plt.xlabel("Day of Week")
plt.ylabel("Compliance Rate (%)")
plt.legend()
plt.tight_layout()
plt.show()

# Time-Based Demand Patterns (When incidents happen)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

# Hourly counts
hourly = df.groupby("HourOfCall")["IncidentNumber"].count()

# Smooth with rolling mean
hourly_smooth = hourly.rolling(window=3, center=True).mean()

plt.figure(figsize=(12,5))
plt.plot(hourly.index, hourly.values, marker="o", alpha=0.4, label="Raw")
plt.plot(hourly.index, hourly_smooth, linewidth=3, label="Smoothed")

plt.title("Fire Incidents by Hour of Day", fontsize=14, fontweight="bold")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Incidents")
plt.xticks(range(0,24))
plt.legend()
plt.show()

# Heatmap: Hour vs Incident Group

heat_data = df.pivot_table(
    index="IncidentGroup",
    columns="HourOfCall",
    values="IncidentNumber",
    aggfunc="count",
    fill_value=0
)

plt.figure(figsize=(14,6))
sns.heatmap(heat_data, cmap="YlOrRd", linewidths=0.3)

plt.title("Incident Distribution: Hour vs Incident Group", fontweight="bold")
plt.xlabel("Hour of Day")
plt.ylabel("Incident Group")
plt.show()

# 6-Minute Target KPI

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df_sub = df[df["BoroughName"].isin(["WESTMINSTER", "HAVERING"])].copy()

target = 360

sns.set_style("whitegrid")

plt.figure(figsize=(12,6))

# KDE plots
sns.kdeplot(
    data=df_sub,
    x="FirstPumpArriving_AttendanceTime",
    hue="BoroughName",
    fill=True,
    palette="rainbow",
    alpha=0.4
)

# Target line
plt.axvline(target, color="red", linestyle="--", linewidth=2)

# --- Add borough labels (annotation) ---
west_mean = df_sub[df_sub["BoroughName"]=="WESTMINSTER"]["FirstPumpArriving_AttendanceTime"].mean()
hav_mean = df_sub[df_sub["BoroughName"]=="HAVERING"]["FirstPumpArriving_AttendanceTime"].mean()


plt.title("6-Minute Target Compliance Distribution (Westminster vs Havering)")
plt.xlabel("Response Time (seconds)")
plt.ylabel("Density")

plt.show()

# Yearly Trend Analysis

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df_sub = df[df["BoroughName"].isin(["WESTMINSTER", "HAVERING"])].copy()

# Safe datetime handling
df_sub["DateOfCall"] = pd.to_datetime(df_sub["DateOfCall"], errors="coerce")
df_sub["Year"] = df_sub["DateOfCall"].dt.year

df_sub = df_sub.dropna(subset=["Year"])

# Convert seconds to minutes
df_sub["ResponseTime_Min"] = df_sub["FirstPumpArriving_AttendanceTime"] / 60

# Yearly aggregation
yearly = df_sub.groupby(["Year", "BoroughName"])["ResponseTime_Min"].mean().reset_index()

sns.set_style("whitegrid")

plt.figure(figsize=(12,6))

sns.lineplot(
    data=yearly,
    x="Year",
    y="ResponseTime_Min",
    hue="BoroughName",
    marker="o",
    palette=["red", "blue"]
)

plt.title("Yearly Trend of Fire Response Time (Minutes)")
plt.xlabel("Year")
plt.ylabel("Average Response Time (minutes)")
plt.legend(title="Borough")

plt.show()

# Save Final Data

# save data set for further processing in Power BI
df.to_csv(
    r"D:\PycharmProjects\Project-London-Fire-Brigade\data\df_final.csv",
    index=False
)