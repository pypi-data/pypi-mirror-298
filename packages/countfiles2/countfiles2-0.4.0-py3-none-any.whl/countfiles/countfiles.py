#!/usr/bin/env python3

import argparse
import os
from typing import List

import colorama
from colorama import Fore, Style

from . import __version__


class Node:
    children: "List[Node]"

    def __init__(self, path: str):
        self.path = path.rstrip("/")
        self.basename = self.path.split("/")[-1]
        self.filecount = 0
        self.children = []

        with os.scandir(self.path) as it:
            for entry in it:
                if entry.is_file():
                    self.filecount += 1
                elif entry.is_dir() and not entry.is_symlink():
                    self.add_child(entry.path)

    def __repr__(self) -> str:
        return f"[{str(self.filecount).rjust(10)}]  {self.basename}"

    def add_child(self, path: str):
        child = Node(path)
        self.filecount += child.filecount
        self.children.append(child)

    def print(self, max_depth=None, min_filecount=None, depth=0, prefix="", is_last_child=False, color=True):
        if color and not depth:
            colorama.init()

        if depth:
            print(prefix, end="")
            if is_last_child:
                print("└── ", end="")
            else:
                print("├── ", end="")

        output = f"[{str(self.filecount).rjust(10)}]  "
        if color:
            output += Fore.LIGHTWHITE_EX + Style.BRIGHT
        output += self.basename

        if min_filecount:
            children = [c for c in self.children if c.filecount >= min_filecount]
        else:
            children = self.children

        if (max_depth and max_depth == depth + 1 and children) or len(self.children) > len(children):
            if color:
                output += Fore.LIGHTBLACK_EX + Style.NORMAL
            output += "*"

        if color:
            print(output + Style.RESET_ALL)
        else:
            print(output)

        if children and (max_depth is None or max_depth > depth + 1):
            if not depth:
                child_prefix = ""
            elif is_last_child:
                child_prefix = prefix + "    "
            else:
                child_prefix = prefix + "│   "
            for idx, child in enumerate(children):
                child.print(
                    max_depth=max_depth,
                    min_filecount=min_filecount,
                    depth=depth + 1,
                    prefix=child_prefix,
                    is_last_child=idx == len(children) - 1,
                    color=color
                )


def cli():
    parser = argparse.ArgumentParser(prog="countfiles", description="Show accumulated number of files per directory.")

    parser.add_argument("path", type=str)
    parser.add_argument(
        "--max-depth", "-md", type=int,
        help="Iterate all the way, but only show directories down to this depth."
    )
    parser.add_argument(
        "--min-filecount", "-mfc", type=int,
        help="Iterate all the way, but only show directories with this number of files or more."
    )
    parser.add_argument("--no-color", action="store_true")
    parser.add_argument("--version", "-V", action="version", version="%(prog)s " + __version__)

    args = parser.parse_args()

    root = Node(args.path)
    root.print(max_depth=args.max_depth, min_filecount=args.min_filecount, color=not args.no_color)

    if args.max_depth or args.min_filecount:
        print("")
        print("* = one or more immediate subdirectories have been omitted")


if __name__ == "__main__":
    cli()
