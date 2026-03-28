from pathlib import Path
import pandas as pd


def load_data(file_path):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Path not found: {file_path}")

    if path.is_dir():
        raise IsADirectoryError(f"Expected a CSV file but got a directory: {file_path}")

    if path.suffix.lower() != ".csv":
        raise ValueError(f"Expected a .csv file but got: {file_path}")

    df = pd.read_csv(path)

    for col in df.columns:
        if "date" in col.lower():
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

    return df