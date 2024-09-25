# bongsang/datasets/__init__.py

import pandas as pd
import importlib.resources


def load_house():
    """
    Load the house.csv dataset.

    Returns:
        pandas.DataFrame: The house dataset.
    """
    with importlib.resources.open_text("bongsang.datasets", "house.csv") as f:
        return pd.read_csv(f)
