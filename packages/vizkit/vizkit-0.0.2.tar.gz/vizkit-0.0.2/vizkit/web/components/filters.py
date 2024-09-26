from typing import Literal, cast, TYPE_CHECKING
import uuid
import streamlit as st
from .flex import flexbox
import pandas as pd

from vizkit.pipeline.utils import (
    scenario_columns,
    value_columns,
)

if TYPE_CHECKING:
    from vizkit.pipeline.blocks import ScenarioFilter, ValueFilter


def scenario_filters(
    data: pd.DataFrame,
    filters: list["ScenarioFilter"],
    initial: list["ScenarioFilter"],
    key: str,
):
    """Render a list of scenario filters, and returns the latest filters."""
    from vizkit.pipeline.blocks import ScenarioFilter

    scenario_cols = scenario_columns(data)
    outer_key = key
    for i, filter in enumerate(filters):
        key = filter._id
        initial_filter = [f for f in initial if f._id == key]
        initial_filter = initial_filter[0] if len(initial_filter) > 0 else None
        with flexbox(children_styles=["", "flex: 1", "flex: 1"]):
            # Delete button
            if st.button("❌", key=f"{key}-remove"):
                filters.pop(i)
                st.rerun()
            # Column selector
            v = initial_filter.column if initial_filter else None
            initial_index = scenario_cols.index(v) if v and v in scenario_cols else None
            col = st.selectbox(
                "Scenario",
                scenario_cols,
                index=initial_index,
                label_visibility="collapsed",
                placeholder="Scenario",
                key=f"{key}-col",
            )
            # Operation selector
            ops = ["includes", "excludes"]
            v = initial_filter.op if initial_filter else None
            initial_index = ops.index(v) if v and v in ops else None
            op = st.selectbox(
                "Operation",
                ops,
                index=initial_index,
                label_visibility="collapsed",
                placeholder="op",
                key=f"{key}-op",
            )
        # Values selector
        candidates: list[str] = (
            sorted(list(set(data[col].astype(str)))) if col in data.columns else []
        )
        initial_values = initial_filter.values if initial_filter else None
        values = st.multiselect(
            "Values",
            candidates,
            default=initial_values,
            label_visibility="collapsed",
            placeholder="Values",
            key=f"{key}-values",
        )
        assert op is None or op in ["includes", "excludes"]
        op = cast(Literal["includes", "excludes"], op or "includes")
        filters[i].column = col or ""
        filters[i].op = op
        filters[i].values = values
        st.write("")
        st.write("")
    if st.button("Add Filter", key=f"{outer_key}-add", use_container_width=True):
        filters.append(ScenarioFilter(column="", op="includes", values=[]))
        st.rerun()
    return filters


def value_filters(
    data: pd.DataFrame,
    filters: list["ValueFilter"],
    initial: list["ValueFilter"],
    key: str,
):
    from vizkit.pipeline.blocks import ValueFilter

    outer_key = key
    value_cols = value_columns(data, ci=False)
    for i, filter in enumerate(filters):
        key = filter._id
        initial_filter = [f for f in initial if f._id == key]
        initial_filter = initial_filter[0] if len(initial_filter) > 0 else None
        with flexbox(children_styles=["", "flex: 1"]):
            # Delete button
            if st.button("❌", key=f"{key}-remove"):
                assert filters is not None
                filters.pop(i)
                st.rerun()
            # Column selector
            v = initial_filter.column if initial_filter else None
            initial_index = value_cols.index(v) if v and v in value_cols else None
            col = st.selectbox(
                "Column",
                value_cols,
                index=initial_index,
                label_visibility="collapsed",
                placeholder="Column",
                key=f"{key}-col",
            )
            # Operation selector
            ops = ["in", "out"]
            v = initial_filter.op if initial_filter else None
            initial_index = ops.index(v) if v and v in ops else None
            op = st.selectbox(
                "Operation",
                ops,
                index=initial_index,
                label_visibility="collapsed",
                placeholder="op",
                key=f"{key}-op",
            )
        # Values selector
        initial_values = initial_filter.range if initial_filter else None
        with flexbox(children_styles=["flex: 1", "flex: 1"]):
            lower = st.number_input(
                "Lower",
                value=initial_values[0] if initial_values else 0.0,
                label_visibility="collapsed",
                placeholder="Lower",
                key=f"{key}-lower",
            )
            upper = st.number_input(
                "Upper",
                value=initial_values[1] if initial_values else 0.0,
                label_visibility="collapsed",
                placeholder="Upper",
                key=f"{key}-upper",
            )
        assert op is None or op in ["in", "out"]
        op = cast(Literal["in", "out"], op or "in")
        filters[i].column = col or ""
        filters[i].op = op
        filters[i].range = (lower, upper)
        st.write("")
        st.write("")
    if st.button("Add Filter", key=f"{outer_key}-add", use_container_width=True):
        filters.append(ValueFilter(column="", op="in", range=(0.0, 0.0)))
        st.rerun()
    return filters
