import enum
import locale
import os

import colorama
from colorama import Fore, Style


class SortBy(enum.Enum):
    NAME = 1
    FILECOUNT = 2
    SIZE = 3


class Node:
    children: "list[Node]"

    def __init__(self, path: str, count_dirs: bool = False, show_sizes: bool = False):
        self.path = path.rstrip("/")
        self.basename = self.path.split("/")[-1]
        self.filecount = 0
        self.size = 0
        self.children = []
        self.count_dirs = count_dirs
        self.show_sizes = show_sizes

        with os.scandir(self.path) as it:
            for entry in it:
                if entry.is_file():
                    self.filecount += 1
                    if self.show_sizes:
                        self.size += entry.stat().st_size
                elif entry.is_dir():
                    if self.count_dirs:
                        self.filecount += 1
                    if not entry.is_symlink():
                        self.add_child(entry.path)

    def __lt__(self, other):
        return isinstance(other, Node) and self.basename.lower() < other.basename.lower()

    def __repr__(self) -> str:
        return f"[{str(self.filecount).rjust(10)}]  {self.basename}"

    def add_child(self, path: str):
        child = Node(path, count_dirs=self.count_dirs, show_sizes=self.show_sizes)
        self.filecount += child.filecount
        self.size += child.size
        self.children.append(child)

    def format_size(self) -> str:
        terabytes = round(self.size / 1024 / 1024 / 1024 / 1024, 1)
        if terabytes >= 1.0:
            return locale.str(terabytes) + "T"
        gigabytes = round(self.size / 1024 / 1024 / 1024, 1)
        if gigabytes >= 1.0:
            return locale.str(gigabytes) + "G"
        megabytes = round(self.size / 1024 / 1024, 1)
        if megabytes >= 1.0:
            return locale.str(megabytes) + "M"
        kilobytes = round(self.size / 1024, 1)
        if kilobytes >= 1.0:
            return locale.str(kilobytes) + "K"
        return str(self.size)

    def get_children(self, sort_by: SortBy, reverse: bool, min_filecount: int | None):
        children = self.children
        if min_filecount:
            children = [c for c in children if c.filecount >= min_filecount]
        match sort_by:
            case SortBy.NAME:
                children = sorted(children, key=lambda c: c.basename, reverse=reverse)
            case SortBy.FILECOUNT:
                children = sorted(children, key=lambda c: c.filecount, reverse=reverse)
            case SortBy.SIZE:
                children = sorted(children, key=lambda c: c.size, reverse=reverse)
        return children

    def print(
        self,
        max_depth: int | None = None,
        min_filecount: int | None = None,
        depth: int = 0,
        prefix: str = "",
        is_last_child: bool = False,
        color: bool = True,
        sort_by: SortBy = SortBy.NAME,
        reverse: bool = False,
    ):
        if color and not depth:
            colorama.init()

        if depth:
            print(prefix, end="")
            if is_last_child:
                print("└── ", end="")
            else:
                print("├── ", end="")

        output = f"[{str(self.filecount).rjust(6)}"
        if self.show_sizes:
            output += f"; {self.format_size().rjust(6)}"
        output += "]  "

        if color:
            output += Fore.LIGHTWHITE_EX + Style.BRIGHT
        output += self.basename

        children = self.get_children(sort_by=sort_by, reverse=reverse, min_filecount=min_filecount)

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
                    color=color,
                    sort_by=sort_by,
                    reverse=reverse,
                )
