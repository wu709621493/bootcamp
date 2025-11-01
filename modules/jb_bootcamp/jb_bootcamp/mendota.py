"""Utilities for working with Lake Mendota data sets."""

from __future__ import annotations

from pathlib import Path
from typing import Final

import pandas as pd

_DATA_PATH: Final = Path(__file__).resolve().parents[3] / "data"


def load_lake_mendota_lai() -> pd.DataFrame:
    """Return Lake Mendota light attenuation index time series.

    The returned data frame contains the following columns.

    ``date``
        Observation date as a timezone-naive :class:`~pandas.Timestamp`.
    ``secchi_m``
        Secchi depth in meters from the North Temperate Lakes LTER program.
    ``light_attenuation_index``
        Empirical light attenuation index (m⁻¹) computed with ``1.7 / secchi_m``.
    """

    csv_path = _DATA_PATH / "mendota_lake_lai.csv"
    data = pd.read_csv(csv_path, parse_dates=["date"])  # type: ignore[arg-type]
    data.sort_values("date", inplace=True)
    data.reset_index(drop=True, inplace=True)
    return data
