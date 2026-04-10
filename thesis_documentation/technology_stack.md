# Technology Stack

## Core Technologies
- **Language**: Python 3.14+
- **Environment**: Jupyter Notebooks (`.ipynb`), Python Scripts (`.py`)

## Key Libraries & Tools
### Data Analysis & Processing
- **Pandas**: Primary library for data manipulation, cleaning, and analysis (DataFrames, CSV reading/writing).
- **NumPy**: Used for numerical operations and array handling.
- **Built-in Modules**: `json` (configuration/data), `os` (file system operations).

## Data Pipeline Architecture
The calibration analysis pipeline validates, processes, and analyzes telemetry data through a sequence of notebooks:

1.  **Data Ingestion**: Raw telemetry logs and death event datasets.
2.  **Processing Steps**:
    *   **Integrity Check**: Validates data structure and completeness.
    *   **Mode Profiling**: Computes descriptive statistics and behavioral fingerprints.
    *   **Survey Analysis**: Aggregates subjective participant feedback.
3.  **Reporting**:
    *   **Automated Reporting**: Generates academic-tone Markdown reports (e.g., `calibration_final_report.md`) directly from analysis scripts.

## Configuration & Storage
- **Configuration**: JSON files (e.g., `config/feature_roles.json`) define metric roles and system parameters.
- **Data Storage**: Processed data is stored in CSV format (`data/processed/`) for transparency and interoperability.

