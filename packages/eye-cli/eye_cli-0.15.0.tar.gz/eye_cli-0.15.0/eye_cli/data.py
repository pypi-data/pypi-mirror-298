from pathlib import Path
from typing import Optional

import inquirer
import pyperclip
import typer
from rich import print
from typing_extensions import Annotated
from yaspin import yaspin
from yaspin.spinners import Spinners

from eye_cli.util import message, color, cmd

app = typer.Typer()


APP_NAME = "eye-cli"
BUCKET = "gs://gecko-chase-photogrammetry-dev"
CAPTURE = f"{BUCKET}/capture"
LOCAL = Path.home() / "Downloads" / "bucket"
LOCAL_CAPTURE = LOCAL / "capture"


def ensure(p: Path):
    p.mkdir(parents=True, exist_ok=True)


@app.command()
def config():
    app_dir = typer.get_app_dir(APP_NAME)
    config_path: Path = Path(app_dir) / "config.json"
    if not config_path.is_file():
        message("No config present", padding="around")
    else:
        message("You have a config", padding="around")


@app.command()
def bucket(preview: bool = True, testing: bool = False):
    m = color("UPLOAD", "red")
    message(f"{m} your whole bucket", padding="around")
    paths = []
    attached = [d / "bucket" for d in Path("/Volumes").iterdir()]
    paths.extend(attached)
    paths.append(LOCAL)
    paths = [d for d in paths if d.is_dir()]

    let_me = "Let me specify..."
    paths.append(let_me)

    paths = [str(p) for p in paths]
    path = inquirer.list_input("Where is your bucket?", choices=paths)

    if path == let_me:
        message(
            f"{color("NOT IMPLEMENTED", "red")} specify your own path", padding="around"
        )
        # prompt for path
        return

    message(f"{color("UPLOAD BUCKET", "red")} from {path}", padding="above")

    message("╮", indent=4)
    for i in Path(path).iterdir():
        message(f"├── {str(i.name)}", indent=4)
    message("╯", indent=4)

    to_path = (
        "gs://gecko-chase-photogrammetry-dev/testing/"
        if testing
        else "gs://gecko-chase-photogrammetry-dev/"
    )
    to_path = f'"{to_path}"'
    message(f"{color("TO", "red")} to {to_path}", padding="below")
    path = f'"{path}"'

    if not inquirer.confirm(
        "Are you sure you want to upload everything here?", default=False
    ):
        message(f"{color("ABORTED", "yellow")}", padding="around")
        return

    args = ["gsutil", "-m", "rsync", "-r"]
    if preview:
        args.append("-n")
    args.extend([path, to_path])

    command = " ".join(args)
    message(f"{color("RUN THIS TO UPLOAD", "green")}  {command}", padding="above")
    message(
        f"{color(" └────> copied to your clipboard paste", "yellow")}", padding="below"
    )
    pyperclip.copy(command)


@app.command()
def capture(name: Annotated[Optional[str], typer.Argument()] = None):
    if not name:
        print()
        name = inquirer.list_input("Which project?", choices=get_folders("capture"))

    message(f"{color("CAPTURE", "green")} {name}", padding="around")


@app.command()
def down(name: str):
    m = color("DOWNLOAD", "green")
    message(f"{m} {name}", padding="around")

    from_path = f"{CAPTURE}/{name}"
    to = LOCAL_CAPTURE / name
    ensure(to)

    f = color(from_path, "blue")
    t = color(to, "orange")
    message(f"{m}\n{f} ->\n{t}", padding="around")

    cmd(["gsutil", "-m", "rsync", "-r", from_path, to])


@app.command()
def folders(path=""):
    for r in get_folders(path=path):
        message(r, indent=4)


@yaspin(Spinners.aesthetic, text="Grabbing folders...", color="yellow")
def get_folders(path=""):
    res = cmd(["gsutil", "ls", f"{BUCKET}/{path}"])
    paths = res.stdout.split("\n")
    results = [p.split("/")[-2] for p in paths if p and p.split("/")[-1] == ""]
    results.sort(key=lambda s: s.lower())
    return results


if __name__ == "__main__":
    app()
