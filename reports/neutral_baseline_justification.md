# Neutral Baseline Justification Report

**Generated**: 2026-03-22 18:39:59  
**Source Analysis**: `03_parameter_derivation.ipynb`  
**Selected Baseline**: **Mode 1**

---

## Neutrality Selection Criteria

The neutral baseline is selected using a composite scoring algorithm that evaluates three key dimensions:

### 1. **Balanced Activity** (Low Sparsity)

*Goal*: Ensure the mode elicits engagement across all gameplay dimensions (Combat, Exploration, Collection).

- **Metric**: Mean sparsity percentage across all tracked metrics
- **Interpretation**: Lower sparsity indicates consistent player activity
- **Mode 1 Performance**: 46.49% mean sparsity

**Why this matters**: A neutral baseline should not favor one archetype over others. High sparsity in any dimension (e.g., 80%+ zero values for combat metrics) suggests that gameplay mechanic is underutilized, indicating imbalance.

### 2. **Stability** (Low Variance)

*Goal*: Ensure predictable, consistent gameplay without extreme fluctuations.

- **Metric**: Mean standard deviation across all metrics
- **Interpretation**: Lower variance indicates stable, non-chaotic gameplay
- **Mode 1 Performance**: 296.13 mean std dev

**Why this matters**: High variance suggests unpredictable gameplay—either death cascades (repeated failures) or boredom streaks (long periods of inactivity). A neutral baseline should provide consistent challenge.

### 3. **Safety** (Manageable Death Rate)

*Goal*: Death rate should be low enough to avoid frustration, but non-zero to confirm meaningful challenge exists.

- **Metric**: Mean deaths per 30-second window
- **Interpretation**: Rate closest to 0 (but not exactly 0) is ideal
- **Mode 1 Performance**: 0.0495 deaths/window

**Why this matters**: Zero deaths suggest trivial difficulty (mode is too easy). Frequent deaths (>0.2/window) suggest frustration. The neutral baseline should challenge players without overwhelming them.

---

## Composite Scoring Algorithm

The neutrality score is a weighted combination of the above criteria:

```
NeutralityScore = (MeanSparsity × 1.0) + (DeathRate × 100.0) + (MeanStdDev × 0.1)
```

**Lower scores = more neutral**

### Score Breakdown:

| Mode | Sparsity | Death Rate | Std Dev | **Neutrality Score** |
|------|----------|------------|---------|----------------------|
| 1 | 46.49% | 0.0495 | 296.13 | **81.05** |
| 2 | 43.24% | 0.0980 | 297.82 | **82.82** |
| 3 | 51.08% | 0.2230 | 319.78 | **105.36** |

→ **Mode 1 achieves the lowest neutrality score**, indicating it best satisfies all three criteria.

---

## Why Other Modes Do Not Qualify

### Mode 3 — Upper Bound (High Difficulty)

**Neutrality Score**: 105.36 (highest)

- **Death Rate**: 0.2230 deaths/window → Significantly higher than Mode 1
- **Interpretation**: This mode is **too difficult**. High death frequency suggests frustration and skill ceiling issues.
- **Classification**: **Upper Difficulty Bound** — Not suitable as neutral baseline, but useful for understanding player tolerance thresholds.

### Mode 2 — Lower Bound

**Neutrality Score**: 82.82

- **Sparsity**: 43.24%
- **Death Rate**: 0.0980 deaths/window
- **Interpretation**: While close to neutral, slight differences in balance or engagement make Mode 1 the optimal choice.
- **Classification**: Alternative reference point for minimum engagement.

---

## Conclusion

**Mode 1** is selected as the **Neutral Baseline** because it:

1. ✓ Maintains balanced activity across all gameplay archetypes (Combat, Exploration, Collection)
2. ✓ Exhibits stable, predictable gameplay without extreme variance
3. ✓ Presents manageable challenge (non-zero deaths without frustration)

This mode represents the **Goldilocks zone** for calibration: not too easy, not too hard, and not favoring any single playstyle.

**Next Steps**:

- Initial PCG parameters are locked based on Mode 1's behavioral profile
- Calibration phase is **complete**
- Future telemetry will be used strictly for **adaptive model training**, not calibration refinement
