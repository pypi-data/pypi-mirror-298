from pathlib import Path
import sys

import pytest

from opla import opla


def test_argparse():
    parser = opla.get_parser()

    args = parser.parse_args([])
    assert args.mdfile == opla.DEFAULT_MD_FILE
    assert args.output == Path("build")

    args = parser.parse_args(["mysite.md"])
    assert args.mdfile == Path("mysite.md")

    args = parser.parse_args(["-o", "output"])
    assert args.output == Path("output")


def test_main(tmp_path):
    data = """\
---
title: Ma page perso
name: Joanna
occupation: Chargée de recherche
theme: 
    name: materialize
    color: teal
---
## Section 1

Section 1 content - Section 1 content Section 1 content - Section 1 content Section 1 content - Section 1 content
Section 1 content - Section 1 content
Section 1 content - Section 1 content

## Section 2

### Section 2.1

Section 2.1 content Section 2.1 content - Section 2.1 content

### Section 2.2

Section 2.2 content Section 2.2 content - Section 2.2 content
Section 2.2 content Section 2.2 content - Section 2.2 content"""

    with open(tmp_path / "test.md", "w") as f:
        f.write(data)
    file = tmp_path / "test.md"
    dir = tmp_path / "dirtest"
    sys.argv = ["opla", str(file), "-o", str(dir)]
    opla.main()
    assert (dir / "index.html").exists()

    # Test file not found
    sys.argv = ["opla", "afilethatdoesnotexist.md"]
    code = opla.main()
    assert code == 1