# Neutral Baseline Justification Report

**Generated**: 2026-04-16 01:23:19  
**Source Analysis**: `03_parameter_derivation.ipynb`  
**Selected Baseline**: **Mode 2**

---

## Neutrality Selection Criteria

The neutral baseline is selected using a composite scoring algorithm that evaluates three key dimensions:

### 1. **Balanced Activity** (Low Sparsity)

*Goal*: Ensure the mode elicits engagement across all gameplay dimensions (Combat, Exploration, Collection).

- **Metric**: Mean sparsity percentage across all tracked metrics
- **Interpretation**: Lower sparsity indicates consistent player activity
- **Mode 2 Performance**: 43.24% mean sparsity

**Why this matters**: A neutral baseline should not favor one archetype over others. High sparsity in any dimension (e.g., 80%+ zero values for combat metrics) suggests that gameplay mechanic is underutilized, indicating imbalance.

### 2. **Stability** (Low Variance)

*Goal*: Ensure predictable, consistent gameplay without extreme fluctuations.

- **Metric**: Mean standard deviation across all metrics
- **Interpretation**: Lower variance indicates stable, non-chaotic gameplay
- **Mode 2 Performance**: 297.82 mean std dev

**Why this matters**: High variance suggests unpredictable gameplay-either death cascades (repeated failures) or boredom streaks (long periods of inactivity). A neutral baseline should provide consistent challenge.

### 3. **Safety** (Manageable Death Rate)

*Goal*: Death rate should be low enough to avoid frustration, but non-zero to confirm meaningful challenge exists.

- **Metric**: Mean deaths per 30-second window
- **Interpretation**: Rate closest to 0 (but not exactly 0) is ideal
- **Mode 2 Performance**: 0.0980 deaths/window

**Why this matters**: Zero deaths suggest trivial difficulty (mode is too easy). Frequent deaths (>0.2/window) suggest frustration. The neutral baseline should challenge players without overwhelming them.

---

## Composite Scoring Algorithm

The neutrality score is a weighted combination of the above criteria:

```
NeutralityScore = (MeanSparsity x 1.0) + (DeathRate x 100.0) + (MeanStdDev x 0.1)
```

**Lower scores = more neutral**

### Score Breakdown:

| Mode | Sparsity | Death Rate | Std Dev | **Neutrality Score** |
|------|----------|------------|---------|----------------------|
| 2 | 43.24% | 0.0980 | 297.82 | **-0.75** |
| 1 | 46.49% | 0.0495 | 296.13 | **-0.59** |
| 3 | 51.08% | 0.2230 | 319.78 | **1.35** |

-> **Mode 2 achieves the lowest neutrality score**, indicating it best satisfies all three criteria.

---

## Why Other Modes Do Not Qualify

### Mode 3 - Upper Bound (High Difficulty)

**Neutrality Score**: 1.35 (highest)

- **Death Rate**: 0.2230 deaths/window -> Significantly higher than Mode 2
- **Interpretation**: This mode is **too difficult**. High death frequency suggests frustration and skill ceiling issues.
- **Classification**: **Upper Difficulty Bound** - Not suitable as neutral baseline, but useful for understanding player tolerance thresholds.

### Mode 1 - Lower Bound

**Neutrality Score**: -0.59

- **Sparsity**: 46.49%
- **Death Rate**: 0.0495 deaths/window
- **Interpretation**: While close to neutral, slight differences in balance or engagement make Mode 2 the optimal choice.
- **Classification**: Alternative reference point for minimum engagement.

---

## Conclusion

**Mode 2** is selected as the **Neutral Baseline** because it:

1. [done] Maintains balanced activity across all gameplay archetypes (Combat, Exploration, Collection)
2. [done] Exhibits stable, predictable gameplay without extreme variance
3. [done] Presents manageable challenge (non-zero deaths without frustration)

This mode represents the **Goldilocks zone** for calibration: not too easy, not too hard, and not favoring any single playstyle.

**Next Steps**:

- Initial PCG parameters are locked based on Mode 2's behavioral profile
- Calibration phase is **complete**
- Future telemetry will be used strictly for **adaptive model training**, not calibration refinement
