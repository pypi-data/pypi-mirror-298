from dataclasses import dataclass
from typing import Literal, override
import numpy as np
import pandas as pd
import streamlit as st

from ..utils import scenario_columns, value_columns
from . import Block


@dataclass
class GraphBlock(Block):
    title: str = "Graph"
    type: Literal["graph"] = "graph"

    format: Literal["Histogram"] = "Histogram"

    # Bar chart configs
    x: str | None = None
    ys: list[str] | None = None
    hue: str | None = None

    @override
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        return data

    def plot(self, data: pd.DataFrame):
        match self.format:
            case "Histogram":
                self.__plot_bar_chart(data)

    def __plot_bar_chart(self, original_data: pd.DataFrame):
        if not self.x or not self.ys:
            return

        # transform column names: replace "." with ":"
        data = original_data.copy()
        for col in data.columns:
            if "." in col:
                data[col.replace(".", ":")] = data[col]
                del data[col]
        x, ys, hue = self.x, self.ys, self.hue
        original_x = x
        x = x.replace(".", ":")
        original_ys = self.ys
        ys = [y.replace(".", ":") for y in ys]
        hue = hue.replace(".", ":") if hue else None

        all_vcols = value_columns(data, ci=True)
        xs: list[str] = list(data[x].unique())
        hues: list[str] = list(data[hue].unique()) if hue else []
        for i, y in enumerate(ys):
            original_y = original_ys[i]
            has_ci = y + ":ci95-lo" in all_vcols and y + ":ci95-hi" in all_vcols
            cols = [x, hue, y] if hue else [x, y]
            cols += [y + ":ci95-lo", y + ":ci95-hi"] if has_ci else []
            df = data.copy()[cols]
            pivot = pd.pivot_table(df, values=y, index=x, columns=hue)
            min, max = pivot.apply(np.min, axis=0), pivot.apply(np.max, axis=0)
            mean = pivot.apply(np.mean, axis=0)
            geomean = pivot.apply(lambda x: np.exp(np.mean(np.log(x))), axis=0)

            def to_df(s, name: str):
                return pd.DataFrame({hue: s.index, y: s.values, x: [name] * len(s)})

            min, max = to_df(min, "min"), to_df(max, "max")
            mean, geomean = to_df(mean, "mean"), to_df(geomean, "geomean")
            gap_symbol = " "
            gap = pd.DataFrame({x: [gap_symbol]})
            df = pd.concat([df, gap, min, max, mean, geomean], ignore_index=True)
            order = [*xs, gap_symbol, "min", "max", "mean", "geomean"]
            layer = [
                {
                    "mark": {"type": "bar", "tooltip": True},
                    "encoding": {
                        "x": {
                            "field": x,
                            "axis": {"labelAngle": -45},
                            "sort": [*order],
                        },
                        "y": {
                            "field": y,
                            "type": "quantitative",
                            "axis": {"title": original_y},
                        },
                        "xOffset": {"field": hue},
                        "color": {"field": hue},
                    },
                }
            ]
            if has_ci:
                layer.append(
                    {
                        "mark": {
                            "type": "errorbar",
                            "extent": "ci",
                            "ticks": {"color": "black"},
                            "size": 5,
                        },
                        "encoding": {
                            "y": {
                                "field": y + ":ci95-hi",
                                "type": "quantitative",
                                "scale": {"zero": False},
                                "axis": {"title": original_y},
                            },
                            "y2": {"field": y + ":ci95-lo"},
                            "x": {"field": x, "type": "ordinal", "sort": [*order]},
                            "xOffset": {"field": hue, "type": "ordinal"},
                        },
                    },
                )
            g = "&nbsp;"
            label = lambda i, s: f"{g}{g}{g}{i}{g}{g}{s}{g}{g}{g}"
            tab1, tab2 = st.tabs([label("📊", "Chart"), label("🗒️", "Data")])
            with tab1:
                st.vega_lite_chart(
                    df, {"layer": layer}, use_container_width=True, theme=None
                )
            with tab2:
                if hue:
                    d: dict[str, list[str | float | None]] = {
                        gap_symbol: xs + [gap_symbol, "min", "max", "mean", "geomean"]  # type: ignore
                    }
                    for h in hues:
                        d[h] = [None] * len(xs) + [None] * 5  # type: ignore
                    for i, row in df.iterrows():
                        value, hue_name, row_name = row[y], row[hue], row[x]
                        row_index = d[gap_symbol].index(row_name)
                        if value is not None and not np.isnan(value):
                            d[hue_name][row_index] = value
                else:
                    d: dict[str, list[str | float | None]] = {
                        x: xs + [gap_symbol, "min", "max", "mean", "geomean"],  # type: ignore
                        y: [None] * len(xs) + [None] * 5,  # type: ignore
                    }
                    for i, row in df.iterrows():
                        value, row_name = row[y], row[x]
                        row_index = d[x].index(row_name)
                        if value is not None and not np.isnan(value):
                            d[y][row_index] = value

                d2 = pd.DataFrame(d)
                d2.set_index(gap_symbol if hue else x, inplace=True)
                st.dataframe(d2, use_container_width=True)

    @override
    def render(self, data: pd.DataFrame):
        format = self.define_selectbox(
            "**_Format_**", "format", ["Histogram"], default="Histogram", label=True
        )
        match format:
            case "Histogram":
                self.__config_bar_chart(data)

    def __config_bar_chart(self, data: pd.DataFrame):
        scenario_cols = scenario_columns(data)
        self.define_selectbox("X Asis", "x", scenario_cols, default="bench", label=True)

        value_cols = value_columns(data, ci=False)
        self.define_multiselect(
            "Y Axis", "ys", value_cols, default=["time"], label=True
        )

        scenario_cols2 = scenario_columns(data, exclude=self.x)
        self.define_selectbox("Hue", "hue", scenario_cols2, default="build", label=True)
