#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import wilcoxon

# Load the original data
file_path = '/Volumes/Extreme SSD/WienUni/Master Thesis (Marmosets)/MM Marmosets/Marmoset exel/Restructured Data for Analysis_zero_out.csv'
df = pd.read_csv(file_path)

# 📌 Behavioral variables to analyze (e.g., Gaze Duration, Head Swaying Frequency, Tsik Frequency)
behaviors = [
    "Total duration (s)_Gaze",
    "Total number of occurences_Head Swaying",
    "Total number of occurences_Tsik (Single Tsik)"
]

# 📌 Define Familiar vs Unfamiliar condition sets
condition_familiar = ["Familiar_match", "Familiar_unmatch"]
condition_unfamiliar = ["Unfamiliar_match", "Unfamiliar_unmatch"]

# 📌 Type conversion for behavioral columns (string → numeric)
for behavior in behaviors:
    df[behavior] = pd.to_numeric(df[behavior], errors="coerce")

# 📌 Compute per-subject averages within Familiar vs Unfamiliar conditions
df_grouped = df.groupby(["Subject_", "Conditions_"]).mean(numeric_only=True).reset_index()

# 📌 Store Wilcoxon Signed-Rank Test results
wilcoxon_results = {}

for behavior in behaviors:
    # Mean within Familiar conditions per subject
    familiar_data = df_grouped[df_grouped["Conditions_"].isin(condition_familiar)].groupby("Subject_")[behavior].mean()
    
    # Mean within Unfamiliar conditions per subject
    unfamiliar_data = df_grouped[df_grouped["Conditions_"].isin(condition_unfamiliar)].groupby("Subject_")[behavior].mean()
    
    # Drop NaNs (required)
    familiar_data = familiar_data.dropna()
    unfamiliar_data = unfamiliar_data.dropna()
    
    # Run Wilcoxon Signed-Rank Test only when paired lengths match and n > 0
    if len(familiar_data) == len(unfamiliar_data) and len(familiar_data) > 0:
        stat, p_value = wilcoxon(familiar_data, unfamiliar_data)
        wilcoxon_results[behavior] = round(p_value, 4)
    else:
        wilcoxon_results[behavior] = None  # Not enough paired data

# 📌 Visualization (add Wilcoxon p-values in titles)
for behavior in behaviors:
    plt.figure(figsize=(8, 6))
    
    # Create Familiar vs Unfamiliar label
    df_plot = df.copy()
    df_plot["Familiarity"] = df_plot["Conditions_"].apply(lambda x: "Familiar" if x in condition_familiar else "Unfamiliar")
    
    # Ensure numeric and drop NaNs for plotting
    df_plot[behavior] = pd.to_numeric(df_plot[behavior], errors="coerce")
    df_plot = df_plot.dropna(subset=[behavior])
    
    # Boxplot with condition-specific colors
    sns.boxplot(data=df_plot, x="Familiarity", y=behavior, palette={"Familiar": "blue", "Unfamiliar": "red"})
    
    # Y-axis label switch (Duration vs Frequency)
    y_label = "Duration" if "duration" in behavior.lower() else "Frequency"
    plt.ylabel(y_label)
    
    # Set plot title (include Wilcoxon p-value; formatting adjusted)
    behavior_label = "Gaze Duration" if "Gaze" in behavior else \
                     "Head Swaying Frequency" if "Head Swaying" in behavior else \
                     "Tsik (Single Tsik) Frequency"
    
    p_value_text = f"Wilcoxon p = {wilcoxon_results[behavior]:.4f}" if wilcoxon_results[behavior] is not None else "Wilcoxon p = N/A"
    plt.title(f"{behavior_label} by Familiarity ({p_value_text})")

    plt.xlabel("Familiarity")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
