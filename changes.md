# Changelog

## [2026-01-18 08:05] Initial Protocol Implementation - Calibration Data
### Added
- Created `generate_calibration_dataset.ipynb`: Jupyter notebook to load telemetry and death events, and construct the aligned calibration dataset.
  - Implemented "Nearest Following Window" alignment rule (`Death Time <= Telemetry Time`).
  - Added derived indicators: `deathOccurredInWindow` (binary) and `deathCountInWindow` (count).
- Created `README.md`: Detailed "Calibration Data Preparation Protocol" and academic justification.
- Created `changes.md`: This file, to track project history for future handover/AI context.

### Methodology Notes
- **Alignment Logic**: Deaths are mapped to the telemetry window that *contains* matching the `userId` and `modeId`. 
- **Handling Multiple Deaths**: If multiple deaths fall within one window, `deathCountInWindow` will reflect the total count (e.g., 2 or 4), while `deathOccurredInWindow` remains 1.

## [2026-01-18 09:15] Calibration Analysis Phase (Steps 1-7)
### Added
- Created 3 Analysis Notebooks for the "Post-Dataset Construction" phase:
  - `01_integrity_check.ipynb`: Validates userId/modeId coverage and data pauses.
  - `02_mode_profiling.ipynb`: Computes per-mode behavioral fingerprints (Mean, Variance, Sparsity).
  - `03_parameter_derivation.ipynb`: Selects Neutral Baseline and derives PCG parameters.
- Created `config/feature_roles.json`: External configuration to define "Combat", "Exploration", and "Collection" metrics, preventing analysis bias.
- Updated `README.md` to include validation and analysis protocols.

## [2026-01-19] Survey Integration & Final Calibration Report
### Added
- Created `04_survey_analysis.ipynb`: Processes participant questionnaire data (7 participants), aggregates mode-level votes and median ratings.
  - Computes vote counts for "most balanced" (Mode 2: 6/7 votes), "too easy" (Mode 1: 5/7 votes), "too difficult" (Mode 3: 4/7 votes).
  - Transformsikert scales to numeric values for median computation.
  - **Output**: `data/processed/survey_summary.csv`, `data/processed/survey_rankings.json`
- Created `05_baseline_justification.ipynb`: Enhances existing gameplay analysis with detailed neutrality explanations.
  - Explains why Mode 1 satisfies neutrality criteria (lowest composite score: 84.21).
  - Flags Mode 3 as upper difficulty bound, Mode 2 as lower bound.
  - **Output**: `reports/neutral_baseline_justification.md`, `data/processed/mode_classifications.json`
- Created `06_calibration_report.py`: Integrates objective (telemetry) and subjective (survey) results into academic report.
  - Analyzes alignment discrepancy: Objective selected Mode 1 (neutral), subjective preferred Mode 2 (balanced perception).
  - Justifies prioritizing objective neutrality for calibration baseline generalizability.
  - Declares formal end of calibration phase and start of adaptive training phase.
  - **Output**: `reports/calibration_final_report.md`
- Created `reports/` directory for markdown outputs.
- Updated `README.md` with documentation for notebooks 04-06.

### Methodology Notes
- **Mode Mapping**: Survey labels (Mode A/B/C) mapped to telemetry IDs (1/2/3) via username cross-reference.
- **Likert Transformation**: Text ratings (e.g., "5 (Very fair)") parsed to numeric; categorical values (e.g., "Balanced" → 3) mapped semantically.
- **Median over Mean**: Used median ratings due to small sample size (n=7) to reduce outlier impact.
- **Alignment Analysis**: Objective (Mode 1) vs. Subjective (Mode 2) discrepancy explained: calibration prioritizes behavioral neutrality over subjective enjoyment for baseline generalizability.
- **No Model Retraining**: Existing mode selection logic from `03_parameter_derivation.ipynb` remains unchanged; new notebooks provide explanatory documentation only (Phase 2) or independent subjective analysis (Phase 1).
- **Calibration Closure**: Final report explicitly declares calibration phase complete and future telemetry will be used exclusively for adaptive model training.
