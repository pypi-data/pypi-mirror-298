import warnings

import typer

# Here to ignore the warning from yaspin
# about running in Jupyter
# TODO make this a more specific ignore
warnings.filterwarnings("ignore", category=UserWarning)

from . import vms
from . import data

cli = typer.Typer()
cli.add_typer(data.app, name="data")
cli.add_typer(vms.app, name="vms")

