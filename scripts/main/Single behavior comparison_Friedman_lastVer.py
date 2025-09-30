import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from itertools import combinations
import scikit_posthocs as sp


# Load data
file_path = '/Volumes/Extreme SSD/Master phase/MM Marmosets/Marmoset exel/Restructured Data for Analysis_zero_out.csv'
df = pd.read_csv(file_path)

# Variable settings
condition_column = "Conditions_"

# Color mapping by condition
conditions = df[condition_column].unique()
colors = {cond: color for cond, color in zip(conditions, ["red", "blue", "yellow", "green"])}

# Column categorization
duration_columns = [col for col in df.columns if "Total duration (s)_" in col]
frequency_columns = [col for col in df.columns if "Total number of occurences_" in col]

# Extract behavior names
all_duration_behaviors = [col.replace("Total duration (s)_", "") for col in duration_columns]
all_frequency_behaviors = [col.replace("Total number of occurences_", "") for col in frequency_columns]
all_behaviors = sorted(set(all_duration_behaviors + all_frequency_behaviors))

# Variance check helper
def has_variance(groups):
    return all(len(set(group)) > 1 for group in groups)

# Friedman test and collection of significant results
significant_results = []
friedman_results = {}
for behavior in all_behaviors:
    duration_col = f"Total duration (s)_{behavior}"
    frequency_col = f"Total number of occurences_{behavior}"
    
    if duration_col in df.columns:
        groups_duration = [df[df[condition_column] == cond][duration_col].values for cond in df[condition_column].unique()]
        if has_variance(groups_duration):
            friedman_stat, friedman_p = stats.friedmanchisquare(*groups_duration)
            friedman_results[(behavior, "Duration")] = (friedman_stat, round(friedman_p, 5))
            if friedman_p < 0.05:
                significant_results.append((behavior, "Duration", duration_col, friedman_p))
    
    if frequency_col in df.columns:
        groups_frequency = [df[df[condition_column] == cond][frequency_col].values for cond in df[condition_column].unique()]
        if has_variance(groups_frequency):
            friedman_stat, friedman_p = stats.friedmanchisquare(*groups_frequency)
            friedman_results[(behavior, "Frequency")] = (friedman_stat, round(friedman_p, 5))
            if friedman_p < 0.05:
                significant_results.append((behavior, "Frequency", frequency_col, friedman_p))

# Visualization for each single behavior
for behavior in all_behaviors:
    duration_col = f"Total duration (s)_{behavior}"
    frequency_col = f"Total number of occurences_{behavior}"
    
    duration_p = friedman_results.get((behavior, "Duration"), (None, None))[1]
    frequency_p = friedman_results.get((behavior, "Frequency"), (None, None))[1]
    
    if duration_col in df.columns:
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df, x=condition_column, y=duration_col, palette=colors)
        plt.title(f"{behavior} Duration (Friedman p={duration_p:.5f})" if duration_p is not None else f"{behavior} Duration by Condition")
        plt.ylabel("Duration")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    if frequency_col in df.columns:
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df, x=condition_column, y=frequency_col, palette=colors)
        plt.title(f"{behavior} Frequency (Friedman p={frequency_p:.5f})" if frequency_p is not None else f"{behavior} Frequency by Condition")
        plt.ylabel("Frequency")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
