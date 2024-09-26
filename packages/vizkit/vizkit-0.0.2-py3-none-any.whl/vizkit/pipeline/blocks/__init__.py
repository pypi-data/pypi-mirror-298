from dataclasses import dataclass, field
from typing import Self, TypeVar, Optional, Literal, TYPE_CHECKING
import pandas as pd
import streamlit as st
import uuid
import copy
from typing import override


if TYPE_CHECKING:
    from .. import Pipeline

T = TypeVar("T")


@dataclass
class Block:
    title: str = "Block"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self):
        self.__default = copy.deepcopy(self)

    @property
    def default(self) -> Self:
        return self.__default

    def is_fixed_block(self) -> bool:
        return False

    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        """Process data and return the updated table"""
        raise NotImplementedError

    def render(self, data: pd.DataFrame):
        """Render block UI"""
        raise NotImplementedError

    def render_and_process(self, data: pd.DataFrame) -> pd.DataFrame:
        self.render(data)
        return self.process(data)

    @staticmethod
    def create_initial_blocks() -> list["Block"]:
        return [
            ColumnsBlock(),
        ]

    # UI Helpers

    def define_selectbox(
        self,
        name: str,
        field: str,
        options: list[T],
        default: T | None = None,
        label=False,
    ) -> T | None:
        # Find the initial value when the page is loaded, or the default value.
        # This value is passed to st.selectbox, and should be immutable across UI updates.
        initial_value: T | None = default if default in options else None
        if hasattr(self.default, field):
            v = getattr(self.default, field)
            if v in options:
                initial_value = v if v in options else None
        if not initial_value and options:
            initial_value = options[0]
        initial_index = (
            options.index(initial_value)
            if initial_value is not None and initial_value in options
            else None
        )
        v: T | None = st.selectbox(
            name,
            options,
            index=initial_index,
            key=f"{self.id}-{field}",
            label_visibility="collapsed" if not label else "visible",
        )
        setattr(self, field, v)
        return v

    def define_multiselect(
        self,
        name: str,
        field: str,
        options: list[T],
        default: list[T] | None = None,
        label=False,
    ) -> list[T]:
        # Find the initial value when the page is loaded, or the default value.
        # This value is passed to st.multiselect, and should be immutable across UI updates.
        initial_values = [v for v in default if v in options] if default else []
        if hasattr(self.default, field):
            vs = getattr(self.default, field)
            if vs and isinstance(vs, list):
                initial_values = [v for v in vs if v in options]
        if not initial_values and options:
            initial_values = [options[0]]
        v = st.multiselect(
            name,
            options,
            default=initial_values,
            key=f"{self.id}-{field}",
            label_visibility="collapsed" if not label else "visible",
        )
        setattr(self, field, v)
        return v


@dataclass
class AddBlock(Block):
    pipeline: Optional["Pipeline"] = None

    title: str = "Add Block"
    type: Literal["add_block"] = "add_block"

    @override
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        return data

    @override
    def render(self, data: pd.DataFrame):
        from . import ALL_BLOCKS

        exclude = [ColumnsBlock, AddBlock]
        blocks = [x for x in ALL_BLOCKS.values() if x not in exclude]
        with flexbox(children_styles=["flex: 1"], justify_content="flex-end"):
            selected_block = st.selectbox(
                "Block Type",
                blocks,
                format_func=lambda x: x.title,
                label_visibility="collapsed",
                placeholder="Add a block",
                key=f"opt-{self.id}",
            )
            if (
                st.button(
                    "&nbsp;&nbsp;&nbsp;**\\+**&nbsp;&nbsp;&nbsp;",
                    use_container_width=True,
                    type="primary",
                    key=f"{self.id}-block-add",
                )
                and selected_block
            ):
                assert self.pipeline is not None
                try:
                    index = self.pipeline.blocks.index(self)
                except ValueError:
                    index = -1
                if index != len(self.pipeline.blocks) - 1 and index != -1:
                    self.pipeline.blocks[index] = selected_block()
                else:
                    self.pipeline.blocks.append(selected_block())
                st.rerun()


from .data_blocks import *
from .graph_blocks import *


ALL_BLOCKS: dict[str, type[Block]] = {
    "columns": ColumnsBlock,
    "add_block": AddBlock,
    "scenario_filter": ScenarioFilterBlock,
    "value_filter": ValueFilterBlock,
    "aggregate": AggregateBlock,
    "normalize": NormalizeBlock,
    "graph": GraphBlock,
}
