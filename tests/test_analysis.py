import pandas as pd

from NEO_Nature.analysis import run_analysis_pipeline


def test_run_analysis_pipeline_smoke(tmp_path, capsys, monkeypatch):
    # Minimal dataset with required columns. We also include legacy columns so
    # the pipeline can adapt regardless of which merged file format is used.
    df = pd.DataFrame(
        {
            "date": ["2025-01-01", "2025-01-02"],
            "disaster_type": ["Wildfires", "Floods"],
            "diameter_max_m": [1000.0, 1200.0],
            "hazardous": [True, False],
        }
    )

    monkeypatch.chdir(tmp_path)
    (tmp_path / "data").mkdir()
    df.to_csv(tmp_path / "data" / "merged_neo_disaster_data.csv", index=False)

    run_analysis_pipeline()
    out = capsys.readouterr().out
    assert "Same-day correlation" in out
