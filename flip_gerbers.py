#!/usr/bin/env python
# coding: utf-8

import os
from pathlib import Path


def mirror(directory: Path, dry_run=True):
    """
    This function takes a Path to a directory
    containing gerber files and swaps all top and bottom layers.
    This effectively mirrors the complete board. 
    Note that this will also mirror any text on the board, 
    including reference designators.

    If dry_run is set to True (default), this function will not
    do anything except output some mildly useful information on 
    what it would do if dry_run were set to False.
    """

    files = os.listdir(directory)
    gerbers = [file for file in files if ".gbr" in file]

    # temporarily add ".temp" to all bottom gerber files
    for gerber in gerbers:
        if "bottom" in gerber:
            print(f"processing {gerber}")
            newname = gerber + ".temp"
            print(f"renaming {gerber} to {newname}")
            if not dryrun:
                os.rename(cwd / gerber, cwd / newname)

    # rename all top files to bottom files
    # swap all references to top in the gerber file to bottom
    for gerber in gerbers:
        if "top" in gerber:
            print(f"processing {gerber}")
            newname = gerber.replace("top", "bottom")
            print(f"renaming {gerber} to {newname}")
            if not dryrun:
                os.rename(cwd / gerber, cwd / newname)
            with open(cwd / newname) as f:
                text = f.read()
            text = text.replace("Top", "Bottom")
            text = text.replace("top", "bottom")
            text = text.replace("TOP", "BOTTOM")
            if not dryrun:
                with open(cwd / newname, "w") as f:
                    f.write(text)

    # rename all (temporarily renamed) bottom files to top files
    # swap all references to bottom in the gerber file to top
    files = os.listdir(cwd)
    gerbers = [file for file in files if ".temp" in file]
    for gerber in gerbers:
        print(f"processing {gerber}")
        newname = gerber.replace(".temp", "")
        newname = newname.replace("bottom", "top")
        print(f"renaming {gerber} to {newname}")
        if not dryrun:
            os.rename(cwd / gerber, cwd / newname)
        with open(cwd / newname) as f:
            text = f.read()
        text = text.replace("Bottom", "Top")
        text = text.replace("bottom", "top")
        text = text.replace("BOTTOM", "TOP")
        if not dryrun:
            with open(cwd / newname, "w") as f:
                f.write(text)
