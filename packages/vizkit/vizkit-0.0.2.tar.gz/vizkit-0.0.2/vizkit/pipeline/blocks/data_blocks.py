from dataclasses import dataclass, field
from typing import Literal, override
import numpy as np
import pandas as pd
import scipy
import streamlit as st
import uuid
import copy
from streamlit_tree_select import tree_select

from vizkit.web.components.flex import flexbox
import vizkit.web.components.filters as filters

from ..utils import scenario_columns, value_columns
from . import Block


DEFAULT_SCENARIO_COLUMNS = ["build", "bench", "invocation", "iteration"]


@dataclass
class ColumnsBlock(Block):
    title: str = "Columns"
    type: Literal["columns"] = "columns"

    scenario_columns: list[str] | None = None
    value_columns: list[str] | None = None

    def is_fixed_block(self) -> bool:
        return True

    @override
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        return data[[*(self.scenario_columns or []), *(self.value_columns or [])]]

    @override
    def render(self, data: pd.DataFrame):
        value_cols = value_columns(data, ci=True)
        scenario_cols = scenario_columns(data)

        def scenario_column_name(c: str) -> str:
            s = c + " ["
            values = sorted(data[c].unique().tolist())
            all_numeric = all(isinstance(v, (int, float)) for v in values)
            if (
                all_numeric
                and len(values) > 0
                and values[-1] - values[0] == len(values) - 1
            ):
                s += f"{values[0]} .. {values[-1]}"
            elif len(values) == 0:
                s += ""
            else:
                s += str(len(values)) + " values"
            s += "]"
            return s

        nodes = [
            {
                "label": "Scenario Columns",
                "value": "sall",
                "children": [
                    {"label": scenario_column_name(c), "value": "s:" + c}
                    for c in scenario_cols
                ],
            },
            {
                "label": "Value Columns",
                "value": "vall",
                "children": [{"label": c, "value": "v:" + c} for c in value_cols],
            },
        ]
        pre_checked = []
        # Pre-checked scenario columns
        if self.scenario_columns is None:
            # By default select all scenario columns
            pre_checked += [f"s:{s}" for s in scenario_cols]
        else:
            pre_checked += [
                f"s:{s}" for s in self.scenario_columns if s in scenario_cols
            ]
        # Pre-checked value columns
        if self.value_columns is None:
            # By default select "time" only
            pre_checked += ["v:time"] if "time" in value_cols else []
        else:
            pre_checked += [f"v:{v}" for v in self.value_columns if v in value_cols]

        checked: list[str] = tree_select(
            nodes, checked=pre_checked, key=f"{self.id}-ts", expand_on_click=True
        )["checked"]

        # Update scenario columns
        if self.scenario_columns is not None or len(scenario_cols) != 0:
            self.scenario_columns = sorted(
                [c[2:] for c in checked if c.startswith("s:")]
            )
        # Update value columns
        if self.value_columns is not None or len(value_cols) != 0:
            self.value_columns = sorted([c[2:] for c in checked if c.startswith("v:")])


@dataclass
class ScenarioFilter:
    column: str
    op: Literal["includes", "excludes"]
    values: list[str]

    _id: str = field(default_factory=lambda: str(uuid.uuid4().hex))


@dataclass
class ScenarioFilterBlock(Block):
    title: str = "Scenario Filter"
    type: Literal["scenario_filter"] = "scenario_filter"

    filters: list[ScenarioFilter] = field(default_factory=list)

    def __post_init__(self):
        super().__post_init__()
        # Backward compatibility
        if len(self.filters) > 0 and isinstance(self.filters[0], (list, tuple)):
            self.filters = []
            self.default.filters = []
        for i in range(len(self.filters)):
            self.filters[i] = ScenarioFilter(**self.filters[i])  # type: ignore
            self.default.filters[i] = ScenarioFilter(**self.default.filters[i])  # type: ignore

    @override
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        scenario_cols = scenario_columns(data)
        # Apply filters
        for filter in self.filters or []:
            col, op, values = filter.column, filter.op, filter.values
            if col and op and values:
                if op == "includes":
                    data = data[data[col].astype(str).isin(values)]
                elif op == "excludes":
                    data = data[~data[col].astype(str).isin(values)]
        # Remove scenario columns if all values are the same
        data = data[
            [c for c in data.columns if c not in scenario_cols or len(set(data[c])) > 1]
        ]
        return data.reset_index(drop=True)

    @override
    def render(self, data: pd.DataFrame):
        # Add default filter if no filters are present
        scenario_cols = scenario_columns(data)
        if not self.filters and not self.default.filters:
            if "iteration" in scenario_cols:
                x = data["iteration"].max()
                self.filters = [ScenarioFilter("iteration", "includes", [f"{x}"])]
            else:
                col = scenario_cols[0] if len(scenario_cols) > 0 else ""
                self.filters = [ScenarioFilter(col, "includes", [])]
            self.default.filters = copy.deepcopy(self.filters)
        # Build filters UI
        self.filters = filters.scenario_filters(
            data, self.filters, initial=self.default.filters, key=self.id + "-filters"
        )


@dataclass
class ValueFilter:
    column: str
    op: Literal["in", "out"]
    range: tuple[float, float]

    _id: str = field(default_factory=lambda: str(uuid.uuid4().hex))


@dataclass
class ValueFilterBlock(Block):
    title: str = "Value Filter"
    type: Literal["value_filter"] = "value_filter"

    filters: list[ValueFilter] = field(default_factory=list)

    def __post_init__(self):
        super().__post_init__()
        # Backward compatibility
        if len(self.filters) > 0 and isinstance(self.filters[0], (list, tuple)):
            self.filters = []
            self.default.filters = []
        for i in range(len(self.filters)):
            self.filters[i] = ValueFilter(**self.filters[i])  # type: ignore
            self.default.filters[i] = ValueFilter(**self.default.filters[i])  # type: ignore

    @override
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        # Apply filters
        for f in self.filters:
            kind, lower, col, upper = f.op, f.range[0], f.column, f.range[1]
            if kind and col and (lower is not None) and (upper is not None):
                if kind.lower() == "in":
                    data = data[data[col].between(lower, upper)]
                elif kind.lower() == "out":
                    data = data[data[col].between(lower, upper)]
        return data.reset_index(drop=True)

    @override
    def render(self, data: pd.DataFrame):
        value_cols = value_columns(data, ci=False)
        # Add default filter if no filters are present
        if not self.filters and not self.default.filters:
            self.filters = [
                ValueFilter(column=value_cols[0], op="in", range=(0.0, 0.0))
            ]
            self.default.filters = copy.deepcopy(self.filters)
        # Build filters UI
        self.filters = filters.value_filters(
            data, self.filters, initial=self.default.filters, key=self.id + "-filters"
        )


@dataclass
class AggregateBlock(Block):
    title: str = "Aggregate"
    type: Literal["aggregate"] = "aggregate"

    op: str | None = None
    col: str | None = None

    @override
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        if self.op and self.col:
            group_cols = scenario_columns(data, exclude=self.col)
            all_cols = [
                c for c in data.columns if c != self.col and c not in group_cols
            ]
            value_cols = value_columns(data, ci=False)  # discard previous ci columns
            if self.op == "mean":
                groups = data.groupby(group_cols)
                stats = groups[all_cols].agg(["mean", "count", "std", "sem"])
                cols = {}
                conf = 0.95
                for v in value_cols:
                    s = stats[v]
                    mean, count, sem = (s["mean"], s["count"], s["sem"])
                    h = sem * scipy.stats.t.ppf((1 + conf) / 2.0, count - 1)
                    cols[v] = mean
                    cols[v + ":ci95-lo"] = mean - h
                    cols[v + ":ci95-hi"] = mean + h
                    cols[v + ":count"] = count
                    cols[v + ":sem"] = sem
                data = pd.DataFrame(cols)
            elif self.op == "geomean":
                data = data.groupby(group_cols)[all_cols].agg("geomean")
        data = data.reset_index()
        return data

    @override
    def render(self, data: pd.DataFrame):
        scenario_cols = scenario_columns(data)
        with flexbox(children_styles=["flex: 1", "", "flex: 1"]):
            self.define_selectbox("Type", "op", ["mean", "geomean"], default="mean")
            st.html('<span style="text-align: center"><b>over</b></span>')
            self.define_selectbox("Column", "col", scenario_cols, default="invocation")


@dataclass
class NormalizeBlock(Block):
    title: str = "Normalize"
    type: Literal["normalize"] = "normalize"

    target: Literal["scenario", "best_value"] | None = None
    scenario: str | None = None
    scenario_value: str | None = None
    grouping: list[str] | None = None

    def __is_with_ci(self, group: pd.DataFrame, col: str):
        return (
            col + ":ci95-lo" in group.columns
            and col + ":ci95-hi" in group.columns
            and col + ":count" in group.columns
            and col + ":sem" in group.columns
        )

    def __normalize_fn(self, value_cols: list[str]):
        def normalize(group: pd.DataFrame) -> pd.DataFrame:
            conf = 0.95
            baseline = group.loc[group[self.scenario] == self.scenario_value]
            for c in value_cols:
                if self.__is_with_ci(group, c):
                    # References:
                    #   1. Fieller's theorem: https://en.wikipedia.org/wiki/Fieller%27s_theorem
                    #   2. Motulsky, 'Intuitive Biostatistics', pp285-6, 'Confidence Interval of a Ratio of Two Means'
                    #   3. Harvey Motulsky (https://stats.stackexchange.com/users/25/harvey-motulsky), How to compute the confidence interval of the ratio of two normal means, URL (version: 2016-05-11): https://stats.stackexchange.com/q/16354
                    val = group[c] / baseline[c].iloc[0]
                    tinv = scipy.stats.t.ppf(
                        (1 + conf) / 2.0,
                        group[f"{c}:count"] + baseline[f"{c}:count"].iloc[0] - 2,
                    )
                    g = (
                        tinv * (baseline[f"{c}:sem"].iloc[0] / baseline[c].iloc[0])
                    ) ** 2
                    sem = (val / (1 - g)) * np.sqrt(
                        (1 - g) * (group[f"{c}:sem"] / group[c]) ** 2
                        + (baseline[f"{c}:sem"].iloc[0] / baseline[c].iloc[0]) ** 2
                    )
                    group[f"{c}:ci95-lo"] = (val / (1 - g)) - tinv * sem
                    group[f"{c}:ci95-hi"] = (val / (1 - g)) + tinv * sem
                    group[c] = val
                    group.pop(f"{c}:count")
                    group.pop(f"{c}:sem")
                else:
                    group[c] = group[c] / baseline[c].iloc[0]
            return group

        return normalize

    @override
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        # process data
        if self.target == "scenario":
            value_cols = value_columns(data, ci=False)
            if self.scenario and self.scenario_value and self.grouping:
                data = data.groupby(self.grouping).apply(
                    self.__normalize_fn(value_cols)
                )
                data = data.reset_index(drop=True)
        elif self.target == "best_value":
            st.error("Not implemented")
        return data

    @override
    def render(self, data: pd.DataFrame):
        kind = st.radio(
            "Normalize to",
            ["To Specific Scenario", "To Best Value"],
            label_visibility="collapsed",
            key=f"{self.id}-kind",
        )
        self.target = "scenario" if kind == "To Specific Scenario" else "best_value"
        # get scenario and value columns
        scenario_cols = scenario_columns(data)
        # get scenario values
        if self.target == "scenario":
            col1, col2 = st.columns([1, 1])
            with col1:
                self.define_selectbox(
                    "Scenario", "scenario", scenario_cols, default="build"
                )
            with col2:
                scenario_vals = sorted(list(set(data[self.scenario])))
                self.define_selectbox(
                    "Value",
                    "scenario_value",
                    sorted(list(set(data[self.scenario]))),
                    default=scenario_vals[0] if len(scenario_vals) > 0 else None,
                )
        # get grouping columns
        grouping_scenario_cols = (
            scenario_columns(data, exclude=self.scenario)
            if self.target == "scenario"
            else scenario_cols
        )
        self.define_multiselect(
            "Grouping", "grouping", grouping_scenario_cols, default=["bench"]
        )
