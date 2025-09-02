# Mpox-Wastewater-Surveillance-Exploratory-Data-Analysis-and-Visualisation

This repository contains exploratory data analysis (EDA) of the **CDC Wastewater Data for Mpox (HMPXV)**.  
The dataset spans from **July 2022 through August 2025** and includes wastewater monitoring data from sewersheds across the United States.

---

## Dataset Overview
- **Rows / Columns:** 184,943 × 39  
- **Time Coverage:** 2022-07-06 → 2025-08-26  
- **Sewersheds Represented:** 747  
- **States Represented:** 51  
- **PCR Targets:** `hmpxv`, `hmpxv clade i`, `hmpxv clade ii`, `nvo`  

Each row corresponds to a wastewater sample, with fields that describe the location, assay target, method, limits of detection, and concentrations.

---

## Data Processing
Steps performed:
1. **Parsing Dates** – Converted `sample_collect_date` and `date_updated` to datetime.  
2. **Type Conversion** – Coerced numeric fields (concentrations, flow rates, recovery metrics).  
3. **Feature Engineering**  
   - `week` (Sunday-start) from the collection date  
   - `state` from FIPS codes  
   - `detected` flag: 1 if measured concentration ≥ limit of detection, else 0  
4. **Cleaning** – Handled missing values, removed records without meaningful detection info.  

---

## Analyses Performed
- **National trends (weekly median concentration)** per PCR target  
- **Weekly detection rates** (share of samples above LOD) per PCR target  
- **State-level detection rates** for Clade II (restricted to states with ≥200 samples)  
- **Overall detection fractions** per target across all years  

---

## Key Figures
Figures are stored in [`outputs/mpox_eda_outputs/`](outputs/mpox_eda_outputs/). Highlights include:

- **Weekly Median Concentration** – Each target’s temporal dynamics  
- **Weekly Detection Rate** – Fraction of positives over time  
- **Top 10 States (Clade II detection rate)** – Comparing surveillance intensity by geography  

---

## Findings
- Wastewater signal for Mpox emerges in **mid-2022**, with a **sharp surge in late 2022**.  
- **Clade II** dominated detections during the 2022 outbreak, with **low but persistent signals** afterward.  
- **Clade I** detections are **sporadic and rare** through 2025.  
- Several states show **higher detection fractions**, but results reflect **variable coverage and methods**.  
- Overall, wastewater monitoring provides an **early-warning, population-level view** of Mpox circulation.  

---

## Caveats
- **LOD variability** – Detection thresholds differ across labs and matrices.  
- **Coverage bias** – Not all states or sewersheds participate equally.  
- **Aggregation choice** – National medians are robust but may not reflect population-weighted burden.  
- **Missing data** – Some records lack key measurements, which may bias detection rates downward.  
