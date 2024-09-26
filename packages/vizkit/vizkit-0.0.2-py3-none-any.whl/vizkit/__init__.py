import argparse
from dataclasses import dataclass
from pathlib import Path
import os


@dataclass
class Options:
    path: Path | None
    firebase: bool
    port: int
    open: bool
    running_ng: bool = False

    @property
    def domain(self) -> str:
        import streamlit as st
        if domain := os.environ.get("DOMAIN"):
            d = domain
        elif host := st.context.headers.get("Host"):
            scheme = "https" if "localhost" not in host else "http"
            d = f"{scheme}://{host}"
        else:
            d = f"http://localhost:{self.port}"
        while d.endswith("/"):
            d = d[:-1]
        return d

    def validate(self):
        if self.path:
            assert self.path.is_dir(), f"{self.path} is not a directory"
            self.path = self.path.resolve()
        if self.firebase:
            assert not self.path, "Cannot use --firebase with a path"

    @staticmethod
    def get() -> "Options":
        import streamlit as st

        @st.cache_resource
        def get_options():
            return Options.parse()

        return get_options()

    @staticmethod
    def parse():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "path",
            nargs="?",
            help="path to the logs directory. default to the current directory",
        )
        parser.add_argument(
            "--firebase",
            action="store_true",
            help="fetch log files from firebase and enable auth guards",
        )
        parser.add_argument(
            "--port",
            type=int,
            default=8501,
            help="port to run the streamlit server on",
        )
        parser.add_argument(
            "--open",
            action="store_true",
            help="open the browser after starting the server",
        )
        parser.add_argument(
            "--running-ng",
            action="store_true",
            help="Use running-ng log files as local data source (instead of csv files). This cannot be used with --firebase",
        )
        options = parser.parse_args()
        firebase = options.firebase or False
        path = (
            Path(options.path)
            if options.path
            else (Path(".") if not firebase else None)
        )
        port = options.port
        running_ng = options.running_ng
        if running_ng and firebase:
            raise ValueError("Cannot use --running-ng with --firebase")
        options = Options(
            path=path,
            firebase=firebase,
            port=port,
            open=options.open,
            running_ng=running_ng,
        )
        return options
