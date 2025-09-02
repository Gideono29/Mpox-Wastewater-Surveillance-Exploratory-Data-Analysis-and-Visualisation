"""

This script performs exploratory data analysis on the CDC Wastewater Data for Mpox.
It reproduces the results and visualizations described in the README.md.

Usage:
    python analysis_script.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ----------------------------
# Configuration
# ----------------------------
DATA_PATH = "data/CDC_Wastewater_Data_for_Mpox.csv"
OUTPUT_DIR = "outputs/mpox_eda_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ----------------------------
# Load Data
# ----------------------------
print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

# ----------------------------
# Data Cleaning & Processing
# ----------------------------
print("Cleaning dataset...")

# Parse dates
df['sample_collect_date'] = pd.to_datetime(df['sample_collect_date'], errors='coerce')
df['date_updated'] = pd.to_datetime(df['date_updated'], errors='coerce')

# Convert numeric fields
numeric_cols = ['conc_cp_ml', 'conc_cp_gsolids', 'flowrate_mgd',
                'solids_mass_g', 'percent_solid', 'percent_recovery']
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Add features
df['week'] = df['sample_collect_date'].dt.to_period('W').dt.start_time
df['detected'] = (df['conc_cp_ml'] >= df['lod_cp_ml']).astype(float)

# ----------------------------
# Summary Stats
# ----------------------------
print("Computing summary statistics...")

n_rows, n_cols = df.shape
n_sewersheds = df['sewershed_id'].nunique()
n_states = df['state'].nunique()
date_min, date_max = df['sample_collect_date'].min(), df['sample_collect_date'].max()

print(f"Rows: {n_rows}, Cols: {n_cols}")
print(f"Sewersheds: {n_sewersheds}, States: {n_states}")
print(f"Date Range: {date_min} → {date_max}")

# ----------------------------
# Analysis & Visualization
# ----------------------------

sns.set_theme(style="whitegrid")

# 1. Weekly median concentration by target
weekly_conc = (df.dropna(subset=['conc_cp_ml'])
                 .groupby(['week', 'pcr_target'])['conc_cp_ml']
                 .median()
                 .reset_index())

plt.figure(figsize=(12,6))
sns.lineplot(data=weekly_conc, x='week', y='conc_cp_ml', hue='pcr_target')
plt.title("Weekly Median Mpox Concentration in Wastewater")
plt.xlabel("Week")
plt.ylabel("Median concentration (cp/mL)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "weekly_median_concentration.png"))
plt.close()

# 2. Weekly detection rate by target
weekly_det = (df.groupby(['week', 'pcr_target'])['detected']
                .mean()
                .reset_index())

plt.figure(figsize=(12,6))
sns.lineplot(data=weekly_det, x='week', y='detected', hue='pcr_target')
plt.title("Weekly Detection Rate of Mpox by Target")
plt.xlabel("Week")
plt.ylabel("Detection rate")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "weekly_detection_rate.png"))
plt.close()

# 3. State-level detection (Clade II)
state_det = (df[df['pcr_target'].str.contains("clade ii", case=False, na=False)]
             .groupby('state')['detected']
             .agg(['mean', 'count'])
             .reset_index())
state_det = state_det[state_det['count'] >= 200].sort_values('mean', ascending=False).head(10)

plt.figure(figsize=(10,6))
sns.barplot(data=state_det, x='mean', y='state', palette='viridis')
plt.title("Top 10 States by Mpox Clade II Detection Rate")
plt.xlabel("Detection rate")
plt.ylabel("State")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "state_top10_detection_rate_clade2.png"))
plt.close()

# 4. Overall detection rate by target
overall_det = (df.dropna(subset=['pcr_target'])
                 .groupby('pcr_target')['detected']
                 .mean()
                 .sort_values(ascending=False)
                 .rename('detection_rate')
                 .to_frame())

overall_det.to_csv("outputs/outputs_overall_detection_rates.csv")
print("Analysis complete. Outputs saved in 'outputs/' folder.")
