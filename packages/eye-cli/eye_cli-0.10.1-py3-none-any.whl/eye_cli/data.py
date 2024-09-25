import typer
import subprocess
from pathlib import Path
from typing import Optional

import inquirer
from rich import print
from rich.padding import Padding
from typing_extensions import Annotated
from yaspin import yaspin
from yaspin.spinners import Spinners




app = typer.Typer()


APP_NAME = "eye-cli"
BUCKET = "gs://gecko-chase-photogrammetry-dev"
CAPTURE = f"{BUCKET}/capture"
LOCAL = Path.home() / 'Downloads' / 'bucket'
LOCAL_CAPTURE = LOCAL / 'capture'


def ensure(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def message(s):
    print(Padding(s, 1))


def color(s, color):
    return f"[bold {color}]{s}[/]"


@app.command()
def config():
    app_dir = typer.get_app_dir(APP_NAME)
    config_path: Path = Path(app_dir) / "config.json"
    if not config_path.is_file():
        message("No config present")
    else:
        message("You have a config")


@app.command()
def bucket():
    m = color("UPLOAD", 'red')
    message(f"{m} whole bucket")


@app.command()
def capture(
        name: Annotated[Optional[str], typer.Argument()] = None):
    if not name:
        print()
        name = inquirer.list_input(
            "Which project?",
            choices=get_folders('capture'))

    message(f"{color("CAPTURE", "green")} {name}")


@app.command()
def down(name: str):
    m = color("DOWNLOAD", 'green')
    message(f"{m} {name}")

    from_path = f"{CAPTURE}/{name}"
    to = LOCAL_CAPTURE / name
    ensure(to)

    f = color(from_path, 'blue')
    t = color(to, 'orange')
    message(f"{m}\n{f} ->\n{t}")

    subprocess.run(['gsutil', '-m', 'rsync', '-r', from_path, to], check=True)


@app.command()
def folders(path=''):
    for r in get_folders(path=path):
        print(r)


@yaspin(Spinners.aesthetic, text="Grabbing folders...", color="yellow")
def get_folders(path=''):
    res = subprocess.run(['gsutil', 'ls', f"{BUCKET}/{path}"], check=True, capture_output=True, encoding='utf-8')
    paths = res.stdout.split('\n')
    results = [p.split('/')[-2] for p in paths if p and p.split('/')[-1] == '']
    results.sort(key=lambda s: s.lower())
    return results


if __name__ == '__main__':
    app()
