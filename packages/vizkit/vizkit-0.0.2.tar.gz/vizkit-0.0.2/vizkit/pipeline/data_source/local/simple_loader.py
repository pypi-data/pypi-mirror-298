from pathlib import Path

import pandas as pd
import toml
from vizkit.pipeline.data_source import DataFile, DataFileMeta, DataFiles
from . import DataLoader
from typing import override


class SimpleLoader(DataLoader):
    path: Path

    results: dict[str, Path]
    """Can be .csv files or directories containing a config.toml and results.csv"""

    def __init__(self, path: Path):
        self.path = path
        self.results = {}

    def __refresh(self):
        if not self.path.exists() or not self.path.is_dir():
            self.results = {}
        # For a rust crate: list all log directories
        logs = []
        if (self.path / "Cargo.toml").exists():
            logs_dir = self.path / "target" / "harness" / "logs"
            for d in logs_dir.iterdir():
                if d.name == "latest" or not d.is_dir():
                    continue
                if (d / "config.toml").exists() and (d / "results.csv").exists():
                    logs.append(d.resolve())
        # list all csv files
        logs_csvs = set([d / "results.csv" for d in logs])
        csvs = [p for p in self.path.glob("*.csv") if p not in logs_csvs]
        # construct map
        results = {}
        for log in logs:
            results[log.name] = log
        for csv in csvs:
            results[csv.name] = csv
        self.results = results

    @override
    def list_data_files(self) -> DataFiles:
        self.__refresh()
        return DataFiles(runids=list(self.results.keys()))

    @override
    def load_data_file(self, id: str) -> DataFile:
        self.__refresh()
        path = self.results[id]
        if path.suffix == ".csv":
            return DataFile(
                results=pd.read_csv(path),
                config={},
                meta=DataFileMeta(runid=path.name),
            )
        config = toml.load(path / "config.toml")
        runid = config.get("runid", id)
        return DataFile(
            results=pd.read_csv(path / "results.csv"),
            config=config,
            meta=DataFileMeta(
                runid=runid,
                project=config.get("project") or "<unknown>",
                profile=config["profile"]["name"],
            ),
        )
