
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set file paths
file_paths = {
    "Gaze Duration": '/Volumes/Extreme SSD/WienUni/Master Thesis (Marmosets)/MM Marmosets/Plots_and_coding/Dunn_test_Total_duration_(s)_Gaze.csv',
    "Head Swaying Frequency": '/Volumes/Extreme SSD/WienUni/Master Thesis (Marmosets)/MM Marmosets/Plots_and_coding/Dunn_test_Total_number_of_occurences_Head_Swaying.csv',
    "Tsik(Single Tsik) Frequency": '/Volumes/Extreme SSD/WienUni/Master Thesis (Marmosets)/MM Marmosets/Plots_and_coding/Dunn_test_Total_number_of_occurences_Tsik_(Single_Tsik).csv'
}

# Load Dunn’s test results
dunn_results = {key: pd.read_csv(path, index_col=0) for key, path in file_paths.items()}

# Load the original data
df = pd.read_csv('/Volumes/Extreme SSD/WienUni/Master Thesis (Marmosets)/MM Marmosets/Marmoset exel/Restructured Data for Analysis_zero_out.csv')

# Map display names to the actual behavior columns
behavior_mapping = {
    "Gaze Duration": "Total duration (s)_Gaze",
    "Head Swaying Frequency": "Total number of occurences_Head Swaying",
    "Tsik(Single Tsik) Frequency": "Total number of occurences_Tsik (Single Tsik)"
}

# Extract condition labels
conditions = df["Conditions_"].unique()

# Find significant pairwise comparisons from Dunn’s test (p-value < 0.05)
def find_significant_pairs(dunn_df):
    significant_pairs = []
    for i, cond1 in enumerate(conditions):
        for j, cond2 in enumerate(conditions):
            if i < j:  # avoid duplicates
                p_value = dunn_df.loc[cond1, cond2]
                if p_value < 0.05:
                    significant_pairs.append((cond1, cond2, p_value))
    return significant_pairs

# Color mapping by condition
condition_column = "Conditions_"
conditions = df[condition_column].unique()
colors = {cond: color for cond, color in zip(conditions, ["red", "blue", "yellow", "green"])}


# Visualization: Boxplot + Dunn’s test annotations (revised version)
for behavior, behavior_col in behavior_mapping.items():
    plt.figure(figsize=(10, 6))
    
    # Draw boxplots (apply colors by condition)
    ax = sns.boxplot(data=df, x=condition_column, y=behavior_col, palette=colors)
    
    # Retrieve significant results from Dunn’s test
    significant_pairs = find_significant_pairs(dunn_results[behavior])

    # Draw lines and asterisks for significant differences
    y_max = df[behavior_col].max()  # maximum of Y-axis
    y_offset = y_max * 0.1          # vertical offset for lines/asterisks

    for i, (cond1, cond2, p_value) in enumerate(significant_pairs):
      # get x positions for the two conditions
        x1, x2 = np.where(conditions == cond1)[0][0], np.where(conditions == cond2)[0][0]
        y = y_max + (i+1) * y_offset  # stacked line positions
        
        # draw the bracket line
        plt.plot([x1, x1, x2, x2], [y, y + 0.02, y + 0.02, y], color="black")
        
        # add significance asterisks by p-value threshold
        if p_value < 0.001:
