import pandas as pd

from NEO_Nature.cleaning import _normalize_columns


def test_normalize_columns_adds_expected_fields():
    df = pd.DataFrame(
        {
            "estimated_diameter_max_km": [1.5],
            "estimated_diameter_min_km": [1.0],
            "is_hazardous": [True],
        }
    )

    out = _normalize_columns(df)

    assert "diameter_max_m" in out.columns
    assert "diameter_min_m" in out.columns
    assert "hazardous" in out.columns
    assert out.loc[0, "diameter_max_m"] == 1500.0
    assert out.loc[0, "diameter_min_m"] == 1000.0
    assert bool(out.loc[0, "hazardous"]) is True
