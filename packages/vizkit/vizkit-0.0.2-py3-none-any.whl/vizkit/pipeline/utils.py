import pandas as pd

from typing import TypeVar

DEFAULT_SCENARIO_COLUMNS = [
    "build",
    "bench",
    "alloc",
    "malloc",
    "invocation",
    "iteration",
]


T = TypeVar("T")


def scenario_columns(
    data: pd.DataFrame, *, exclude: list[str] | str | None = None
) -> list[str]:
    if exclude is None:
        exclude = []
    if isinstance(exclude, str):
        exclude = [exclude]
    default_scenarios = [
        c for c in data.columns if c in DEFAULT_SCENARIO_COLUMNS and c not in exclude
    ]
    # any columns with non-numeric values
    non_numeric = [
        c
        for c in data.columns
        if c not in default_scenarios
        and not pd.api.types.is_numeric_dtype(data[c])
        and c not in exclude
    ]
    return default_scenarios + non_numeric


def is_ci_column(col: str) -> bool:
    if ":" not in col:
        return False
    suffix = col.split(":")[-1]
    return suffix in ["ci95-lo", "ci95-hi", "sem", "count"]


def value_columns(
    data: pd.DataFrame, *, ci: bool, exclude: list[str] | str | None = None
) -> list[str]:
    if exclude is None:
        exclude = []
    if isinstance(exclude, str):
        exclude = [exclude]
    return [
        c
        for c in data.columns
        if c not in DEFAULT_SCENARIO_COLUMNS
        and (ci or not is_ci_column(c))
        and c not in exclude
        and pd.api.types.is_numeric_dtype(data[c])
    ]
