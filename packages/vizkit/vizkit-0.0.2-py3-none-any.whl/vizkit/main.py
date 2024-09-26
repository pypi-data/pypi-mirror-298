from pathlib import Path
import sys, os
import streamlit.web.cli as stcli
import dotenv

from vizkit import Options

_WEB_DIR = Path(__file__).parent / "web"


def main():
    dotenv.load_dotenv()
    args = sys.argv[1:]
    options = Options.parse()
    sys.argv = [
        "streamlit",
        "run",
        *(["--server.headless", "true"] if not options.open else []),
        "--server.port",
        str(options.port),
        str(_WEB_DIR / "plot.py"),
    ]
    if len(args) > 0:
        sys.argv += ["--", *args]
    os.environ["PYTHONPATH"] = os.curdir
    sys.exit(stcli.main())
