-Multimodal Recognition in Marmosets-

Master-thesis at the Vienna University
Would marmosets distinguish human?
We hypothese that common marmoset could distinguish familiar human and unfamiliar human
Result = They can distinguish familiar and unfamiliar human through vocal and visual inputs, but they couldn't differenciate each familiar (unfamiliar) members in both human groups


End-to-end flow (paper order)
	1	Behavior–behavior correlation heatmap → 2) PCA loadings & cumulative variance → 3) 3D scatter of top 3 PCs → 4) Single-variable comparisons by condition (Friedman → Dunn + viz) → 5) Familiarity comparison (Wilcoxon, selected behaviors)
Implementation note: PCA_again_lastVer.py already covers Steps 1–3 (heatmap + PCA + 3D).

1–3) Correlation & PCA (heatmap, loadings, 3D scatter)
	•	Script: PCA_again_lastVer.py
	•	Input: Restructured Data for Analysis_zero_out.csv
	•	Outputs:
	◦	Correlation heatmap among behaviors (Pearson by default; optionally add Spearman)
	◦	pc_explained_variance.csv (cumulative variance), PCA_Loadings_Top_8_PCs.csv (top loadings)
	◦	3D scatter of PC1–PC3 (color by Conditions_ recommended)
	•	Diagnostics & assumptions
	◦	Correlation: Pearson assumes approximate linearity/normality; use Spearman as a robust alternative.
	◦	PCA: Z-scored features; be mindful of outliers (robust scaling/transform if needed).
	•	Interpretation
	◦	Use the heatmap to find behavioral clusters, loadings to identify drivers, and 3D scatter to inspect condition separation.

4) Single behavior × condition
	•	Scripts:
	◦	Omnibus: Single behavior comparison_Friedman_lastVer.py
	◦	Post hoc: post hoc_Dunn_lastVer.py → Dunn_test_*.csv
	◦	Visualization: Friedman_Dunn_visualize_lastVer.py (adds brackets/stars)
	•	Input: Restructured Data for Analysis_zero_out.csv (+ Dunn CSVs)
	•	Outputs: Condition-wise boxplots with Friedman p and Dunn post hoc annotations
	•	Why Friedman?
	◦	Nonparametric repeated-measures alternative when normality/homoscedasticity is doubtful and observations are within-subject across conditions.
	•	Diagnostics
	◦	Check group distributions/QQ-plots, Shapiro–Wilk on residuals or differences, and Levene for variance.
	◦	Violations justify nonparametric choice.
	•	Post hoc
	◦	Dunn with multiplicity control (Bonferroni or BH/FDR).
	◦	Report effect sizes: Kendall’s W for Friedman; r for pairwise contrasts.

5) Familiarity comparison (Gaze Duration, Head Swaying)
	•	Script: FamiliarVSUnfamiliar_Wilcoxon_signed_rank_lastVer.py
	•	Input: Restructured Data for Analysis_zero_out.csv
	•	Output: Boxplots with Wilcoxon signed-rank p (same subjects: Familiar vs Unfamiliar)
	•	Why Wilcoxon?
	◦	Paired comparison across two condition sets, robust to non-normality.
	◦	If the difference (Familiar − Unfamiliar) passes Shapiro–Wilk (p≥0.05), a paired t-test is a parametric alternative; otherwise, stay with Wilcoxon.
	•	Optional
	◦	For a between-subjects take, use FamiliarVSUnfamiliar_lastVer.py (Mann–Whitney U) with the dedicated summary table.

Common visualization & reporting
	•	Boxplots with jitter to show distribution and outliers
	•	Add means/medians and CIs (bootstrap CIs are preferable under non-normality)
	•	Multiple-testing control for all post hoc results
	•	Effect sizes matched to the test (r, Kendall’s W, Cliff’s delta, etc.)
	•	Reproducibility: fixed output paths (results/01–05/...), random seeds, versioning
