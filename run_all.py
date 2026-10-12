"""End-to-end: simulate 340 cell-culture batches, characterize 45 CPP
attributes, and compute the viability in-spec rate."""
import json
import os

from src.simulate_cell_culture import simulate
from src.process_characterization import characterize_all_parameters
from src.viability_spec import in_spec_rate

os.makedirs("data", exist_ok=True)
os.makedirs("results", exist_ok=True)

print("=== Simulating 340 cell-culture batches ===")
df = simulate()
df.to_csv("data/batches.csv", index=False)
print(df.shape)

print("\n=== Characterizing 45 critical process parameter attributes ===")
characterization = characterize_all_parameters(df)
characterization.to_csv("results/process_characterization.csv", index=False)
deviation_corr = characterization[characterization["attribute"] == "deviation_correlation_with_viability"]
print(deviation_corr.sort_values("value"))

print("\n=== Viability in-spec rate ===")
spec_result = in_spec_rate(df)
print(spec_result)

summary = {
    "n_batches": spec_result["n_batches"],
    "n_characterization_points": len(characterization),
    "in_spec_rate_pct": spec_result["in_spec_rate_pct"],
    "mean_viability_pct": spec_result["mean_viability_pct"],
    "strongest_cpp_driver": deviation_corr.loc[deviation_corr["value"].idxmin(), "parameter"],
}
with open("results/summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("\n=== Summary ===")
print(json.dumps(summary, indent=2))
