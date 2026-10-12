"""Real viability in-spec rate: the % of batches meeting the standard
cell-culture release specification (viability >= 95%), computed directly
from the simulated batch outcomes."""
from __future__ import annotations

import pandas as pd

VIABILITY_SPEC_MIN = 95.0


def in_spec_rate(df: pd.DataFrame, spec_min: float = VIABILITY_SPEC_MIN) -> dict:
    in_spec = df["viability_pct"] >= spec_min
    return {
        "n_batches": len(df), "n_in_spec": int(in_spec.sum()),
        "in_spec_rate_pct": round(100 * in_spec.mean(), 3),
        "mean_viability_pct": round(float(df["viability_pct"].mean()), 3),
    }


if __name__ == "__main__":
    from .simulate_cell_culture import simulate

    df = simulate()
    print(in_spec_rate(df))
