import pandas as pd
from pathlib import Path


def extract_data():

    project_root = Path(__file__).resolve().parent.parent

    file_path = project_root / "data" / "Sample - Superstore.csv"

    df = pd.read_csv(
        file_path,
        encoding="latin1"
    )

    print(f"Successfully extracted {len(df)} rows")

    return df