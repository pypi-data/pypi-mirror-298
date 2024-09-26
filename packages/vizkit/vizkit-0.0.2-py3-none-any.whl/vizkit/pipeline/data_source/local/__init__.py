import os
from pathlib import Path
import sqlite3
from typing import TYPE_CHECKING
import pandas as pd
import toml
import streamlit as st
from typing import override

from vizkit import Options

from .. import DataSource, DataFiles, DataFile, DataFileMeta


if TYPE_CHECKING:
    from ... import Pipeline


class DataLoader:
    def list_data_files(self) -> DataFiles:
        raise NotImplementedError

    def load_data_file(self, id: str) -> DataFile:
        raise NotImplementedError


class LocalDataSource(DataSource):
    def __init__(self, path: Path) -> None:
        super().__init__()
        if not Options.get().running_ng:
            from .simple_loader import SimpleLoader

            self.loader: DataLoader = SimpleLoader(path)
        else:
            from .running_ng_loader import RunningNGLoader

            self.loader = RunningNGLoader(path)
        self.cache_file = Path(os.curdir) / ".cache" / "vizkit-share-links.db"
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        db_exists = self.cache_file.exists()
        if not db_exists:
            with sqlite3.connect(self.cache_file) as con:
                con.execute(
                    "CREATE TABLE share_links (id TEXT PRIMARY KEY, inflated TEXT);"
                )

    @property
    def is_local(self) -> bool:
        return True

    @override
    def get_inflated_link(self, key: str) -> str | None:
        with sqlite3.connect(self.cache_file) as con:
            c = con.cursor()
            res = c.execute("SELECT inflated FROM share_links WHERE id = ?;", (key,))
            row = res.fetchone()
            if row is None:
                return None
            return row[0]

    @override
    def insert_inflated_link(self, inflated: str) -> str:
        with sqlite3.connect(self.cache_file) as con:
            c = con.cursor()
            # If the inflated pipeline already exists, return the key
            res = c.execute(
                "SELECT id FROM share_links WHERE inflated = ?;", (inflated,)
            )
            row = res.fetchone()
            if row is not None:
                return row[0]
            while True:
                # We use shortuuid to generate a key instead of sql-generated key, so it looks consistent with the firebase implementation.
                key = self._generate_share_link_key()
                # Check if key already exists
                res = c.execute("SELECT id FROM share_links WHERE id = ?;", (key,))
                if res.fetchone() is None:
                    break
            c.execute(
                "INSERT INTO share_links (id, inflated) VALUES (?, ?);", (key, inflated)
            )
            c.close()
        return key

    def list_data_files(self) -> DataFiles:
        return self.loader.list_data_files()

    @override
    def load_data_file(self, id: str) -> DataFile:
        return self.loader.load_data_file(id)

    @override
    def render_data_source_block(self, pipeline: "Pipeline", initial_inputs: list[str]):
        data_ids = self.list_data_files().runids

        with st.sidebar:
            # Data Source selector
            input = initial_inputs[0] if len(initial_inputs) > 0 else None
            initial_index = (
                data_ids.index(input) if input and input in data_ids else None
            )
            selected_data = st.sidebar.selectbox(
                "Data Source",
                data_ids,
                index=initial_index,
            )
            if selected_data:
                pipeline.inputs = [selected_data]
            # Share button
            self._render_share_button(pipeline)
