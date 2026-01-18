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
- Updated `README.md` to include validataion and analysis protocols.
