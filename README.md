# Calibration Data Preparation Protocol

*(Pre-Adaptation Phase of AURA)*

## Position in AURA Pipeline

This process sits **before** behavioural clustering and **after** raw telemetry logging:

**Telemetry (30s windows)**
-> **Calibration Dataset Construction (this step)**
-> Normalisation
-> Behavioural Clustering
-> Percentages + Deltas
-> ANFIS Reasoning Layer
-> Real-Time Procedural Content Adaptation
-> Smoothing
-> Logging

This step **does not perform learning, clustering, or adaptation**.

---

## Objective

The objective of this step is to:

> Construct a **derived, analysis-ready calibration dataset** by temporally aligning raw telemetry windows with discrete death events, while preserving the integrity of the original logs.

This dataset serves **only** to:

* Characterise baseline behavioural tendencies
* Compare gameplay modes under controlled conditions
* Support parameter calibration prior to adaptation activation

---

## Guiding Principles

1. **Raw telemetry is immutable**
   The original telemetry and death logs remain unchanged and archived.

2. **Calibration data is derived, not corrected**
   No values are altered, interpolated, or retroactively smoothed.

3. **Temporal alignment, not inference**
   Death events are *mapped*, not predicted or redistributed.

4. **Reproducibility**
   The same procedure can be re-executed at any time on future datasets.

---

## Process Overview

### Step 1 - Inputs

*   **Telemetry Dataset**: 30-second behavioural observation windows (`userId`, `timestamp`, metrics).
*   **Death Event Dataset**: Discrete terminal events (`userId`, `timestamp`).

### Step 2 - Temporal Alignment Rule

> A death event is associated with the **nearest following telemetry window** for the same user and mode.
> Specifically: `Death Time <= Telemetry Window Time`

This aligns the death with the window that *contains* it (assuming telemetry timestamps mark the end of the window interval).

### Step 3 - Augmentation

The new **Calibration Dataset** includes:
*   `deathOccurredInWindow` (0 or 1)
*   `deathCountInWindow` (Integer count of deaths in that window)

---

## Reusability Statement


---

# Calibration Phase 2: Post-Dataset Construction (Analysis)

*(Steps 1-7 of the Academic Protocol)*

Once the `calibration_dataset.csv` is generated, the following **Analysis Phase** begins. This phase validates integrity, profiles per-mode behaviour, and derives the initial PCG parameters.

## Process Overview - The 3 Notebooks

### 1. Integrity Check (`01_integrity_check.ipynb`)
**Objective**: "Verify that the calibration dataset preserves structural, temporal, and experimental integrity." (Step 1)
*   Verifies every `userId` appears in all `modeId`s.
*   Checks for data corruption (NaNs, negative values).
*   **Must pass** before proceeding.

### 2. Mode Profiling (`02_mode_profiling.ipynb`)
**Objective**: "Compute descriptive statistics for each metric within each mode to establish a behavioural fingerprint." (Steps 2-4)
*   **Feature Roles**: Uses `config/feature_roles.json` to define "Combat", "Exploration", etc. to prevent semantic bias.
*   **Outputs**: `data/mode_profiles.csv`.
*   **Stability Analysis**: detecting "death cascades" or "boredom streaks".

### 3. Parameter Derivation (`03_parameter_derivation.ipynb`)
**Objective**: "Select the neutral baseline and derive initial PCG parameters from Step 3." (Steps 5-7)
*   **Selection**: Automatically scores modes based on balance and stability to find the "Neutral Baseline".
*   **Derivation**: Locks initial PCG parameters (e.g., `EnemyDensity`) based on this baseline.
*   **Transition**: Explicitly declares the end of Calibration and the start of Model Training.

## Calibration Phase 3: Validation & Integration (Final Analysis)

### 4. Survey Analysis (`04_survey_analysis.ipynb`)
**Objective**: "Aggregate participant questionnaire responses to establish subjective mode rankings."
- Computes vote counts for balance categories (most balanced, too easy, too difficult, would play longer)
- Computes median ratings for combat fairness, exploration comfort, collectible availability
- Produces ranked summary of modes based on perceived balance
- **Output**: `data/processed/survey_summary.csv`, `data/processed/survey_rankings.json`
- **Note**: Does NOT merge with gameplay telemetry (independent subjective analysis)

### 5. Baseline Justification (`05_baseline_justification.ipynb`)
**Objective**: "Provide detailed justification for neutral baseline selection from gameplay telemetry."
- Explains why selected mode satisfies neutrality criteria (balance, stability, safety)
- Flags other modes as upper/lower difficulty bounds
- Generates documentation suitable for thesis methodology section
- **Output**: `reports/neutral_baseline_justification.md`, `data/processed/mode_classifications.json`
- **Note**: Does NOT retrain models or change baseline selection (explanatory only)

### 6. Calibration Report (`06_calibration_report.ipynb`)
**Objective**: "Integrate objective and subjective results into academic-tone final report."
- Validates alignment (or analyzes discrepancy) between gameplay and survey analysis
- Justifies final default configuration selection
- Declares formal transition from calibration to adaptive training phase
- **Output**: `reports/calibration_final_report.md`
- **Academic Tone**: Suitable for direct inclusion in thesis methodology/results chapters

## Configuration
*   **`config/feature_roles.json`**: External definition of metric roles. Update this file if the structure of telemetry changes.
