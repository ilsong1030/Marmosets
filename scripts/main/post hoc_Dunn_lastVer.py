import pandas as pd
import scikit_posthocs as sp
import scipy.stats as stats

# Load data
file_path = '/Volumes/Extreme SSD/WienUni/Master Thesis (Marmosets)/MM Marmosets/Marmoset exel/Restructured Data for Analysis_zero_out.csv'
df = pd.read_csv(file_path)


# Set variables to analyze
conditions_col = "Conditions_"
behaviors = [
    "Total duration (s)_Gaze",
    "Total number of occurences_Head Swaying",
    "Total number of occurences_Tsik (Single Tsik)"
]

# Run Dunn's test
dunn_results = {}

for behavior in behaviors:
    # Filter data
    data = df[[conditions_col, behavior]].dropna()
    
    # Perform Dunn's test (with Bonferroni correction)
    dunn_test = sp.posthoc_dunn(data, val_col=behavior, group_col=conditions_col, p_adjust='bonferroni')
    
    # Save results in memory
    dunn_results[behavior] = dunn_test
    
    # Save to CSV file
    file_name = f"Dunn_test_{behavior.replace(' ', '_').replace('/', '_')}.csv"
    dunn_test.to_csv(file_name)

# Print results
for behavior, result in dunn_results.items():
    print(f"\nDunn’s test results for {behavior}:")
    print(result)
