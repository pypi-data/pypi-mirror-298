# vizkit

Data plotting and visualization platform.

## Getting Started

1. `pipx install vizkit`
2. Create a data folder: `mkdir vizkit-example && cd vizkit-example`
3. Put some .csv files into the data folder, for example [this one](https://gist.github.com/wenyuzhao/ec38429b9e176ae922ef70009a553a95).
4. Run `vizkit` to start the server.
   * [Example link](http://localhost:8501/?px=eNptjzsOwjAQRO8ytcUB0tGl4gLIQsZabIN_8idKFOXubEAgCsqdp3maXZFLupNuGGL3XsDF3FvFcAbNKmRPB10nSIGrT_qxgxVtyYQBOvkeYoVA1RRVcenyibh-UoH23qR8p19wNMSVkZyxDXITX58pKltGt1SC4kEYXW2J08DhzPdLKbD80QjYTu8fNrk9AfBAR94%3D).

## Local server with [running-ng](https://anupli.github.io/running-ng/) logs

Run `vizkit --running-ng /path/to/running-ng/logs`

## Generate Reports Using the [Harness](https://github.com/wenyuzhao/harness) Bench Tool

Running a benchmark with the `--upload` flag will automatically upload the results data to [r.harness.rs](https://r.harness.rs).

Example: `harness run --upload`.

## Generate Reports Using [running-ng](https://github.com/anupli/running-ng)

WIP...
