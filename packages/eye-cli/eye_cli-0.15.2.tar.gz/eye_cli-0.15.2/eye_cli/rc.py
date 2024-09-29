from pathlib import Path

import typer

from eye_cli.util import message, color, cmd

app = typer.Typer()

RC = "C:\Program Files\Capturing Reality\RealityCapture\RealityCapture.exe"


def start_rc(name):
    args = [RC, "-setInstanceName", name]
    cmd(args)


def delegate_to_rc(name, args):
    launch = [RC, "-delegateTo", name]
    launch.extend(args)
    cmd(launch)


@app.command()
def simplify(component: str, relative_percent: int = 50, times: int = 1):

    message(color("Simplify", "yellow"), padding="around")

    status = "Found" if Path(RC).is_file() else "Not Found"
    message(f"RC: {color(status, 'yellow')} at: {RC}")

    if not Path(RC).is_file():
        return

    instance = "RC1"
    start_rc(instance)

    settings = [
        ("-selectComponent", component),
        # Means aim for a percentage of the current triangles
        ("-set", "mvsFltSimplificationType=1"),
        # target number of triangles in %
        ("-set", "mvsFltTargetTrisCountRel=50"),
        # this may be saying "leave any edges smaller than this" which could be very useful for keeping little details
        ("-set", "mvsFltMinEdgeLength=0.0"),
        # Simplify Border or no. 1 = Simplify, ? = Keep
        ("-set", "mvsFltBorderDecimationStyle=1"),
        # affects density at part boundaries, select true for quality
        ("-set", "simplEqualizeDensity=true"),
        # when simplified parts get small, merge them? 2 = merge
        ("-set", "simplPreserveParts=2"),
        ### texture reprojection settings - not using
        # Reproject color? may reproject texture
        ("-set", "mvsFltReprojectColor=false"),
        # reproject normals into the new texture. no texture in this case
        ("-set", "mvsFltReprojectNormal=0"),
        # params for retexturing... not using these
        ("-set", "mvsFltUnwrapTexCount=0"),
        ("-set", "mvsFltUnwrapTexSide=0"),
    ]
    for s in settings:
        delegate_to_rc(instance, s)
    delegate_to_rc(instance, ["-save"])

    for i in range(times):
        message(f"simplifying, iteration {i}/{times}")
        delegate_to_rc(instance, ["-simplify"])
        delegate_to_rc(instance, ["-save"])
