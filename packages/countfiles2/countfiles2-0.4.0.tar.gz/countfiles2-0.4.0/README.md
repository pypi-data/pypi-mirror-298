# countfiles

Like `tree` on Linux, but for number of files.

The basics:

```shell
$ countfiles --help
usage: countfiles [-h] [--max-depth MAX_DEPTH] [--min-filecount MIN_FILECOUNT] [--sizes] [--count-dirs] [--reverse] [--no-color] [--version] [--sort-count | --sort-size] [path]

Show accumulated number of files per directory.

positional arguments:
  path

options:
  -h, --help            show this help message and exit
  --max-depth MAX_DEPTH, -d MAX_DEPTH
                        Iterate all the way, but only show directories down to this depth.
  --min-filecount MIN_FILECOUNT, -m MIN_FILECOUNT
                        Iterate all the way, but only show directories with this number of files or more.
  --sizes, -s           Also show the total size of every directory.
  --count-dirs, -c      Also include directories in the file counts.
  --reverse, -r         Reverse result sorting.
  --no-color
  --version, -V         show program's version number and exit
  --sort-count, -sc     Sort results by file count.
  --sort-size, -ss      Sort results by total size.
```

Example output:

```shell
$ countfiles --sizes --max-depth 4
[  1200;  47.2M]  .
├── [    49;  51.8K]  .git
│   ├── [     0;      0]  branches
│   ├── [    12;  18.6K]  hooks
│   ├── [     1;    240]  info
│   ├── [     4;   1.5K]  logs
│   │   └── [     3;     1K]  refs*
│   ├── [    21;    30K]  objects
│   │   ├── [     1;    210]  0b
│   │   ├── [     1;     38]  26
│   │   ├── [     1;    488]  31
│   │   ├── [     1;    589]  34
│   │   ├── [     1;     73]  3e
│   │   ├── [     1;   6.2K]  47
│   │   ├── [     1;     52]  50
│   │   ├── [     1;   1.2K]  6b
│   │   ├── [     1;    550]  8c
│   │   ├── [     2;    220]  9d
│   │   ├── [     1;    549]  a4
│   │   ├── [     1;     55]  a6
│   │   ├── [     1;    114]  b0
│   │   ├── [     1;    930]  c8
│   │   ├── [     1;     38]  d3
│   │   ├── [     1;    218]  d5
│   │   ├── [     1;    218]  d8
│   │   ├── [     1;    113]  f9
│   │   ├── [     0;      0]  info
│   │   └── [     2;  18.4K]  pack
│   └── [     3;    114]  refs
│       ├── [     1;     41]  heads
│       ├── [     2;     73]  remotes*
│       └── [     0;      0]  tags
├── [   218;    14M]  .mypy_cache
│   ├── [    99;   6.5M]  3.11
│   │   ├── [     2; 109.7K]  _typeshed
│   │   ├── [     4; 708.1K]  collections
│   │   ├── [     8;  24.6K]  countfiles
│   │   ├── [    14; 207.2K]  email
│   │   ├── [    10; 268.7K]  importlib*
│   │   └── [     4; 396.9K]  os
│   └── [   117;   7.5M]  3.12
│       ├── [     4; 132.1K]  _typeshed
│       ├── [     4; 830.9K]  collections
│       ├── [     6;  20.8K]  countfiles
│       ├── [    16; 313.4K]  email
│       ├── [    18; 290.6K]  importlib*
│       ├── [     4; 417.4K]  os
│       ├── [     4; 176.4K]  sys
│       └── [     4; 116.7K]  zipfile
├── [   897;    33M]  .venv
│   ├── [    11;  23.1M]  bin
│   ├── [     0;      0]  include
│   │   └── [     0;      0]  python3.12
│   └── [   885;   9.9M]  lib
│       └── [   885;   9.9M]  python3.12*
├── [     4;   8.4K]  build
│   ├── [     0;      0]  bdist.linux-x86_64
│   └── [     4;   8.4K]  lib
│       └── [     4;   8.4K]  countfiles
├── [     6;    778]  countfiles.egg-info
├── [     4;  45.5K]  dist
└── [    17;  61.6K]  src
    ├── [    11;  30.1K]  countfiles
    │   └── [     8;  23.7K]  __pycache__
    └── [     6;  31.6K]  countfiles.egg-info
```
