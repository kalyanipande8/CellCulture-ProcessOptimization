import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from src.simulate_cell_culture import simulate
from src.process_characterization import characterize_all_parameters, PARAMETERS
from src.viability_spec import in_spec_rate


@pytest.fixture(scope="module")
def df():
    return simulate()


def test_340_batches_simulated(df):
    assert len(df) == 340


def test_exactly_45_characterization_points(df):
    result = characterize_all_parameters(df)
    assert len(result) == 45


def test_every_parameter_has_sop_and_equipment_reference(df):
    result = characterize_all_parameters(df)
    for param in PARAMETERS:
        sub = result[result["parameter"] == param]
        assert "sop_reference" in sub["attribute"].values
        assert "equipment_reference" in sub["attribute"].values


def test_ph_deviation_is_the_strongest_driver(df):
    """pH has the strongest built-in effect on viability in the
    simulation -- the characterization should correctly identify it as
    the parameter with the largest-magnitude deviation correlation."""
    result = characterize_all_parameters(df)
    dev_corr = result[result["attribute"] == "deviation_correlation_with_viability"]
    strongest = dev_corr.loc[dev_corr["value"].idxmin(), "parameter"]
    assert strongest == "ph"


def test_in_spec_rate_in_realistic_band(df):
    result = in_spec_rate(df)
    assert 90.0 <= result["in_spec_rate_pct"] <= 100.0


def test_in_spec_rate_not_trivially_perfect(df):
    result = in_spec_rate(df)
    assert result["n_in_spec"] < result["n_batches"]
