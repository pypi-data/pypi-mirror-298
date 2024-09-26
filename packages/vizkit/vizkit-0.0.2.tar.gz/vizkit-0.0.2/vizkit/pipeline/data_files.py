import pandas as pd


class DataFiles:
    def __init__(self, tables: dict[str, pd.DataFrame]) -> None:
        self.tables = tables
        if not tables:
            self.tables = {}

    def dataframe(self) -> pd.DataFrame:
        if len(self.tables) == 1:
            return next(iter(self.tables.values()))
        # add a `file` column to each table
        for fileid, df in self.tables.items():
            df["file"] = fileid
        return pd.concat(self.tables.values(), ignore_index=True)
