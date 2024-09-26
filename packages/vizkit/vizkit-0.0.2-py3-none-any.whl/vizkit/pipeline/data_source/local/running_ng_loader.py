import gzip
from pathlib import Path

import pandas as pd
import toml
from vizkit.pipeline.data_source import DataFile, DataFileMeta, DataFiles
from . import DataLoader
from typing import override
import re


class RunningNGLoader(DataLoader):
    path: Path

    results: dict[str, Path]
    """Directories containing a runbms.yml and runbms_args.yml"""

    def __init__(self, path: Path):
        self.path = path
        self.results = {}

    def __refresh(self):
        if not self.path.exists() or not self.path.is_dir():
            self.results = {}
        # list all log folders files
        folders = [
            p.parent
            for p in self.path.glob("**/*/runbms.yml")
            if p.parent.joinpath("runbms_args.yml").exists()
        ]
        # construct results
        results = {}
        for folder in folders:
            results[folder.name] = folder
        self.results = results

    @override
    def list_data_files(self) -> DataFiles:
        self.__refresh()
        return DataFiles(runids=list(self.results.keys()))

    def __load_log_file(
        self, file: Path
    ) -> tuple[list[dict[str, float | str]], set[str]]:
        assert file.exists() and file.suffix == ".gz"
        # decompress
        with gzip.open(file, "rb") as f:
            lines = f.read().decode().split("\n")

        data: list[dict[str, float | str]] = []
        invocation = -1
        last_iteration = -1
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            # Start of a new invocation
            if line == "-----":
                invocation += 1
            # Warmup completed
            if m := re.match(
                r"===== .* completed warmup (\d+) in (\d+) msec =====", line
            ):
                iteration = int(m.group(1)) - 1
                bmtime = int(m.group(2))
                data.append(
                    {"iteration": iteration, "bmtime": bmtime, "invocation": invocation}
                )
                last_iteration = iteration
                i += 1
                continue
            # Parse stats for final iteration
            if not re.match(r"===== .* starting =====", line):
                i += 1
                continue
            i += 1  # next line
            keys, values, bmtime, time = None, None, None, None
            while i < len(lines):
                if keys is not None and values is not None and bmtime is not None:
                    break
                line = lines[i].strip()
                # stats
                if line.startswith("=" * 28) and line.endswith("=" * 28):
                    i += 1
                    if i >= len(lines):
                        break
                    keys = [x for x in lines[i].strip().split() if x.strip() != ""]
                    i += 1
                    if i >= len(lines):
                        break
                    values = [float(x) for x in lines[i].strip().split() if x != ""]
                    i += 1
                    if i >= len(lines):
                        break
                    line = lines[i].strip()
                    if line.startswith("Total time: "):
                        time = float(line.split()[-2])
                        i += 1
                    i += 1  # Skip the --- ... --- line
                    continue
                # bmtime
                if m := re.match(r"===== .* PASSED in (\d+) msec =====", line):
                    bmtime = int(m.group(1))
                    i += 1
                    continue
                # error
                if line == "-----":
                    break
                i += 1
            if keys is not None and values is not None and bmtime is not None:
                stat: dict[str, float | str] = {k: v for k, v in zip(keys, values)}
                stat["bmtime"] = bmtime
                stat["invocation"] = invocation
                stat["iteration"] = last_iteration + 1
                if time is not None:
                    stat["time"] = time
                data.append(stat)
            i += 1
        # Add other columns
        tokens = file.stem.split(".")
        buildstring = ".".join(tokens[3:-1])
        bench = tokens[0]
        hfac = float(tokens[1])
        heap = float(tokens[2])
        build = tokens[3]
        others = {}
        if len(tokens) > 4:
            for token in tokens[4:-1]:
                others[token] = "Y"
        for d in data:
            d["buildstring"] = buildstring
            d["bench"] = bench
            d["build"] = build
            d["heap"] = heap
            d["hfac"] = hfac
            for k, v in others.items():
                d[k] = v
        return data, set(others.keys())

    def __load_log_files(self, folder: Path) -> pd.DataFrame:
        files = list(folder.glob("*.log.gz"))
        data = []
        all_scenario_cols = set()
        for file in files:
            df, other_scenario_cols = self.__load_log_file(file)
            data.extend(df)
            all_scenario_cols.update(other_scenario_cols)
        for d in data:
            for k in all_scenario_cols:
                if k not in d:
                    d[k] = "N"
        return pd.DataFrame(data)

    @override
    def load_data_file(self, id: str) -> DataFile:
        self.__refresh()
        folder = self.results[id]
        results = self.__load_log_files(folder)
        return DataFile(
            results=results,
            config={},
            meta=DataFileMeta(runid=id),
        )
