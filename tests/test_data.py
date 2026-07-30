import pandas as pd


def test_dataset_exists():
    df = pd.read_csv("data/raw/ethiopia_fi_unified_data.csv")
    assert len(df) > 0


def test_columns_exist():
    df = pd.read_csv("data/raw/ethiopia_fi_unified_data.csv")

    required_columns = [
        "record_type",
        "indicator_code",
        "observation_date"
    ]

    for col in required_columns:
        assert col in df.columns
