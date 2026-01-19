"""
Final Integration Report - Phase 3
===================================
Combines objective (telemetry) and subjective (survey) analyses into academic-tone calibration report.

This script:
1. Loads survey rankings from Phase 1
2. Loads gameplay baseline selection from Phase 2
3. Performs alignment analysis between objective and subjective results
4. Generates academic-tone report suitable for thesis inclusion
5. Declares explicit transition from calibration to adaptive training

This is the FINAL output of the calibration phase.
"""

import pandas as pd
import numpy as np
import json
import os

# ============================================================================
# Configuration
# ============================================================================

DATA_DIR = 'data'
CONFIG_DIR = 'config'
REPORTS_DIR = 'reports'
PROCESSED_DIR = os.path.join(DATA_DIR, 'processed')

# Input files
SURVEY_SUMMARY = os.path.join(PROCESSED_DIR, 'survey_summary.csv')
SURVEY_RANKINGS = os.path.join(PROCESSED_DIR, 'survey_rankings.json')
MODE_CLASSIFICATIONS = os.path.join(PROCESSED_DIR, 'mode_classifications.json')
INITIAL_PARAMS = os.path.join(CONFIG_DIR, 'initial_parameters.json')

# Output file
OUTPUT_REPORT = os.path.join(REPORTS_DIR, 'calibration_final_report.md')

# ============================================================================
# Step 1: Load All Analysis Results
# ============================================================================

print("=" * 70)
print("FINAL INTEGRATION REPORT - PHASE 3")
print("=" * 70)

print("\n[1/4] Loading analysis results from Phases 1 & 2...")

# Load survey results
df_survey = pd.read_csv(SURVEY_SUMMARY)
with open(SURVEY_RANKINGS, 'r') as f:
    survey_rankings = json.load(f)

print(f"      Survey analysis: Loaded rankings for {len(df_survey)} modes")
print(f"      Total participants: {survey_rankings['metadata']['total_participants']}")

# Load gameplay telemetry results
with open(MODE_CLASSIFICATIONS, 'r') as f:
    mode_classifications = json.load(f)

with open(INITIAL_PARAMS, 'r') as f:
    initial_params = json.load(f)

selected_baseline = mode_classifications['selected_baseline']['modeId']
print(f"      Gameplay analysis: Selected baseline is Mode {selected_baseline}")

# ============================================================================
# Step 2: Alignment Analysis
# ============================================================================

print("\n[2/4] Performing alignment analysis...")

# Get subjective rankings
df_survey_ranked = df_survey.sort_values('balance_rank')
subjective_rank_1 = int(df_survey_ranked.iloc[0]['modeId'])
subjective_votes = int(df_survey_ranked.iloc[0]['votes_most_balanced'])
total_participants = survey_rankings['metadata']['total_participants']

# Check if alignment exists
alignment_exists = (subjective_rank_1 == selected_baseline)

print(f"      Objective (Telemetry): Mode {selected_baseline}")
print(f"      Subjective (Survey): Mode {subjective_rank_1} ({subjective_votes}/{total_participants} votes)")
print(f"      Alignment: {'YES ✓' if alignment_exists else 'DISCREPANCY DETECTED'}")

# If discrepancy, analyze why
discrepancy_analysis = ""
if not alignment_exists:
    # Compare metrics
    objective_mode = mode_classifications['selected_baseline']
    subjective_mode_data = df_survey[df_survey['modeId'] == subjective_rank_1].iloc[0]
    
    discrepancy_analysis = f"""
### Discrepancy Analysis

While objective telemetry selected **Mode {selected_baseline}** and subjective survey ranked **Mode {subjective_rank_1}** highest, this discrepancy is instructive:

**Subjective Preference (Mode {subjective_rank_1})**:
- {subjective_votes}/{total_participants} participants voted it "most balanced" ({100*subjective_votes/total_participants:.1f}% agreement)
- Median combat fairness: {subjective_mode_data['median_combat_fairness']:.1f}
- Median exploration comfort: {subjective_mode_data['median_exploration_comfort']:.1f}
- Median collectible availability: {subjective_mode_data['median_collectible_availability']:.1f}

**Objective Selection (Mode {selected_baseline})**:
- Lowest neutrality score: {objective_mode['neutrality_score']:.2f}
- Death rate: {objective_mode['metrics']['death_rate']:.4f}/window
- Mean sparsity: {objective_mode['metrics']['mean_sparsity']:.2f}%

**Interpretation**:
Participants often prefer modes that feel engaging or rewarding (subjective experience), which may not align with objective behavioral neutrality. Mode {selected_baseline} was selected as the calibration baseline because it exhibits the most *statistically balanced* behavioral profile, not necessarily the most *enjoyable* experience. This distinction is critical: calibration seeks a neutral starting point, not an optimal one. The adaptive system will learn player preferences during runtime.
"""
else:
    discrepancy_analysis = f"""
### Alignment Confirmation

Excellent concordance exists between objective and subjective analyses:

- **Objective telemetry**: Mode {selected_baseline} has lowest neutrality score
- **Subjective survey**: Mode {subjective_rank_1} voted "most balanced" by {100*subjective_votes/total_participants:.1f}% of participants

This alignment validates the calibration methodology: the mode that behaves most neutrally from a telemetry perspective also *feels* most balanced to players.
"""

# ============================================================================
# Step 3: Generate Academic Report
# ============================================================================

print("\n[3/4] Generating academic-tone final report...")

report_md = f"""# Calibration Phase: Final Integration Report

**Date**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}  
**System**: AURA (Adaptive User-Responsive Architecture)  
**Phase**: Pre-Adaptation Calibration  
**Status**: **COMPLETE**

---

## 1. Calibration Phase Overview

This report integrates the results of objective gameplay telemetry analysis and subjective participant survey responses to finalize the calibration phase for the AURA adaptive gameplay system.

**Calibration Objective**: Establish a neutral baseline game mode configuration that:
1. Exhibits balanced behavioral engagement across all gameplay archetypes (Combat, Exploration, Collection)
2. Maintains stable, predictable gameplay without extreme variance
3. Presents manageable challenge without frustration

**Data Sources**:
- **Objective**: {mode_classifications['metadata'].get('total_windows', 'Multiple')} telemetry windows from {total_participants} participants across 3 game modes
- **Subjective**: Post-gameplay questionnaire responses from {total_participants} participants

---

## 2. Objective Results: Gameplay Telemetry Analysis

### Methodology

Telemetry data was collected in 30-second windows during blind gameplay sessions. Three modes were presented without difficulty labels to avoid bias. Behavioral profiles were computed for each mode using:

- **Sparsity analysis**: Percentage of windows with zero activity per metric
- **Stability analysis**: Standard deviation of metric values
- **Safety analysis**: Death frequency per window

A composite neutrality score was calculated:

```
NeutralityScore = (MeanSparsity × 1.0) + (DeathRate × 100.0) + (MeanStdDev × 0.1)
```

### Results

| Mode | Neutrality Score | Role |
|------|-----------------|------|
| {selected_baseline} | {mode_classifications['selected_baseline']['neutrality_score']:.2f} | **Neutral Baseline** ✓ |
| {mode_classifications['lower_bound']['modeId']} | {mode_classifications['lower_bound']['neutrality_score']:.2f} | Lower Bound |
| {mode_classifications['upper_bound']['modeId']} | {mode_classifications['upper_bound']['neutrality_score']:.2f} | Upper Bound (High Difficulty) |

**Selected Baseline: Mode {selected_baseline}**

Justification:
- Mean sparsity: {mode_classifications['selected_baseline']['metrics']['mean_sparsity']:.2f}% (balanced activity)
- Death rate: {mode_classifications['selected_baseline']['metrics']['death_rate']:.4f}/window (manageable challenge)
- Mean std deviation: {mode_classifications['selected_baseline']['metrics']['mean_std']:.2f} (stable gameplay)

Mode {selected_baseline} represents the **Goldilocks zone**: not too easy, not too hard, and not favoring any single playstyle.

---

## 3. Subjective Results: Survey Analysis

### Methodology

After completing all three modes, participants answered a comparative questionnaire including:
- Likert scale ratings for combat fairness, exploration comfort, collectible availability
- Categorical votes for "most balanced", "too easy", "too difficult", "would play longer"

Results were aggregated at the mode level. Median ratings were computed to reduce outlier impact in the small sample.

### Results

**Mode Ranking by "Most Balanced" Votes**:

| Rank | Mode | Votes | Percentage |
|------|------|-------|------------|
"""

for idx, item in enumerate(survey_rankings['ranked_by_balance'], start=1):
    mode_id = item['modeId']
    votes = item['votes_most_balanced']
    pct = 100 * votes / total_participants if total_participants > 0 else 0
    marker = "✓" if mode_id == subjective_rank_1 else ""
    report_md += f"| {idx} | {mode_id} | {votes} | {pct:.1f}% {marker} |\n"

report_md += f"""
**Subjective Winner: Mode {subjective_rank_1}**

**Vote Distribution Summary**:
"""

for mode_id in [1, 2, 3]:
    mode_data = df_survey[df_survey['modeId'] == mode_id].iloc[0]
    report_md += f"""
- **Mode {mode_id}**:
  - Most balanced: {mode_data['votes_most_balanced']} votes
  - Too easy: {mode_data['votes_too_easy']} votes
  - Too difficult: {mode_data['votes_too_difficult']} votes
  - Would play longer: {mode_data['votes_would_play_longer']} votes
"""

report_md += f"""
---

## 4. Alignment Discussion: Objective vs. Subjective

{discrepancy_analysis}

---

## 5. Final Configuration Justification

Based on the comprehensive calibration analysis, the following configuration is adopted:

### Default Game Mode: **Mode {selected_baseline}**

**Rationale**:
"""

if alignment_exists:
    report_md += f"""
Mode {selected_baseline} achieves dual validation:
1. **Objective neutrality**: Lowest composite score from telemetry analysis
2. **Subjective preference**: Highest votes for "most balanced" from participants

This concordance provides strong evidence that Mode {selected_baseline} is the optimal neutral baseline for calibration.
"""
else:
    report_md += f"""
While Mode {subjective_rank_1} received the most "balanced" votes subjectively, Mode {selected_baseline} was selected based on *objective behavioral neutrality*. 

The calibration phase prioritizes statistical balance over subjective preference because:
1. **Neutral starting point**: The adaptive system requires an unbiased baseline that doesn't favor specific playstyles
2. **Runtime adaptation**: Player preferences will be learned dynamically during gameplay, not prescribed during calibration
3. **Generalizability**: Behavioral neutrality generalizes better across diverse player populations than small-sample subjective votes

Mode {selected_baseline}'s neutrality score of {mode_classifications['selected_baseline']['neutrality_score']:.2f} indicates it best satisfies the criteria for a calibration baseline.
"""

report_md += f"""
### Initial Parameters

The following PCG parameters are locked based on Mode {selected_baseline}'s behavioral profile:

"""

# List some key parameters
for key, value in list(initial_params.items())[1:6]:  # Skip _meta, show first 5 params
    if key != '_meta':
        report_md += f"- `{key}`: {value:.4f}\\n"

report_md += f"""
*Full parameter specification available in: `config/initial_parameters.json`*

---

## 6. Transition Declaration

### End of Calibration Phase

> **DECLARATION**  
>   
> The Calibration Phase is hereby **COMPLETE**.  
>   
> **Frozen Artifacts**:
> - Calibration dataset (`data/processed/calibration_dataset.csv`)
> - Mode profiles (`data/processed/mode_profiles.csv`)
> - Initial parameters (`config/initial_parameters.json`)
> - Survey summary (`data/processed/survey_summary.csv`)
>   
> These artifacts are **archived** and will not be modified by future telemetry.

### Beginning of Adaptive Training Phase

**Effective Date**: {pd.Timestamp.now().strftime('%Y-%m-%d')}

From this point forward:

1. **New Telemetry Purpose**: All future gameplay telemetry will be used **exclusively for adaptive model training**, not calibration refinement.

2. **No Feedback Loop**: The calibration parameters derived here are **locked**. They will not be updated based on training-phase telemetry.

3. **Model Training**: The AURA adaptive system (behavioral clustering, ANFIS reasoning, PCG adjustment) will now be trained using incoming gameplay data.

4. **Separation of Concerns**:
   - **Calibration data**: Establishes baseline and training targets
   - **Training data**: Teaches the adaptive system to respond to player behavior
   - **Runtime data**: Drives real-time procedural content adaptation

---

## 7. Implications for Thesis Methodology

This calibration report provides the following contributions to the thesis:

### Methodological Rigor

- **Dual Validation**: Both objective telemetry and subjective surveys were employed, demonstrating triangulation of evidence.
- **Transparent Criteria**: The neutrality scoring algorithm is explicitly defined and reproducible.
- **Academic Tone**: Suitable for inclusion in methodology/results chapters.

### Research Validity

- **Baseline Justification**: Mode {selected_baseline} selection is justified through quantitative criteria, not arbitrary choice.
- **Reproducibility**: All analysis notebooks (01-06) can be re-executed on future datasets.
- **Separation of Phases**: Clear boundary established between calibration and training prevents data contamination.

### Future Work

- **Adaptive Performance Evaluation**: Future experiments can compare adaptive system performance against this calibration baseline.
- **Player Preference Modeling**: The discrepancy (if any) between subjective preference and objective neutrality can inform player modeling research.

---

## 8. Conclusion

The calibration phase has successfully established a neutral baseline (Mode {selected_baseline}) for the AURA adaptive gameplay system. This configuration satisfies rigorous criteria for behavioral balance, stability, and safety, {f'and aligns with participant subjective preferences.' if alignment_exists else 'prioritizing objective neutrality over subjective preference for generalizability.'}

**Calibration Phase Status**: ✓ **COMPLETE**  
**Next Phase**: Adaptive Model Training  
**Baseline Configuration**: Mode {selected_baseline}  

---

*This report was generated automatically by `06_calibration_report.ipynb` on {pd.Timestamp.now().strftime('%Y-%m-%d at %H:%M:%S')}.*
"""

with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
    f.write(report_md)

print(f"      Saved final report: {OUTPUT_REPORT}")

# ============================================================================
# Step 4: Summary Output
# ============================================================================

print("\n[4/4] Calibration summary...")

print("\n" + "=" * 70)
print("CALIBRATION PHASE COMPLETE")
print("=" * 70)

print(f"\nSelected Configuration:")
print(f"  Baseline Mode: {selected_baseline}")
print(f"  Neutrality Score: {mode_classifications['selected_baseline']['neutrality_score']:.2f}")
print(f"  Subjective Rank: #{int(df_survey[df_survey['modeId'] == selected_baseline]['balance_rank'].values[0])}")

print(f"\nObjective vs. Subjective:")
if alignment_exists:
    print(f"  ✓ ALIGNED - Mode {selected_baseline} is both objectively neutral and subjectively balanced")
else:
    print(f"  ⚠ DISCREPANCY - Objective selected Mode {selected_baseline}, subjective preferred Mode {subjective_rank_1}")
    print(f"    (Prioritizing objective neutrality for calibration baseline)")

print(f"\nGenerated Outputs:")
print(f"  - {OUTPUT_REPORT}")

print("\n" + "=" * 70)
print("🎯 FINAL REPORT GENERATION COMPLETE")
print("=" * 70)
print("\nCalibration phase is now CLOSED.")
print("All future telemetry will be used for adaptive model training only.")
