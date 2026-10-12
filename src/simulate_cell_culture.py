"""Simulate 340 cell-culture bioreactor batches with process parameters
and a real, mechanistically-driven viability outcome -- pH and dissolved
oxygen excursions genuinely reduce viability, the signal the
characterization step below should recover."""
from __future__ import annotations

import numpy as np
import pandas as pd

N_BATCHES = 340
SEED = 181


def simulate(n: int = N_BATCHES, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    ph = rng.normal(7.0, 0.15, n)
    dissolved_oxygen_pct = rng.normal(45, 8, n)
    temperature_c = rng.normal(37.0, 0.4, n)
    agitation_rpm = rng.normal(120, 15, n)
    glucose_g_l = rng.normal(4.0, 0.8, n)
    osmolality = rng.normal(310, 20, n)

    ph_dev = np.abs(ph - 7.0)
    do_dev = np.abs(dissolved_oxygen_pct - 45)
    temp_dev = np.abs(temperature_c - 37.0)

    viability = 99.5 - 8 * ph_dev - 0.08 * do_dev - 1.5 * temp_dev + rng.normal(0, 0.4, n)
    viability = np.clip(viability, 70, 100)

    return pd.DataFrame({
        "batch_id": [f"BATCH-{i:04d}" for i in range(n)],
        "ph": np.round(ph, 3), "dissolved_oxygen_pct": np.round(dissolved_oxygen_pct, 2),
        "temperature_c": np.round(temperature_c, 3), "agitation_rpm": np.round(agitation_rpm, 1),
        "glucose_g_l": np.round(glucose_g_l, 2), "osmolality_mosm_kg": np.round(osmolality, 1),
        "viability_pct": np.round(viability, 2),
    })


if __name__ == "__main__":
    df = simulate()
    print(df.shape)
    print(df["viability_pct"].describe())
