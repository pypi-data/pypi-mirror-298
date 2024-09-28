"""
Main module for the opla package
"""

import argparse
from pathlib import Path
import sys

from . import __version__
from .payload import create_output_directory, copy_files
from .markdown import parse_markdown_file, create_menu
from .templating import get_template

DEFAULT_MD_FILE = Path("opla.md")


def get_parser():
    """
    Return the parser for the opla command-line interface

    Returns:
        argparse.ArgumentParser: the parser for the opla command-line interface
    """
    parser = argparse.ArgumentParser(
        description=(
            "A professional webpage generator with a focus " "on research activities"
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "mdfile", nargs="?", type=Path, help="markdown file path", default=DEFAULT_MD_FILE
    )
    parser.add_argument(
        "-o", "--output", type=Path, default=Path("build"), help="output directory"
    )

    return parser


def main():
    """
    Generates a personal page by parsing command-line arguments, creating the page content and its menu, renders the HTML template, and writes the result into a HTML file
    """
    parser = get_parser()
    args = parser.parse_args(sys.argv[1:])

    output_directory_path = args.output

    create_output_directory(output_directory_path)

    try:
        header, (sections, _) = parse_markdown_file(args.mdfile)
    except FileNotFoundError:
        # print argparse help message
        print(f"File not found: {args.mdfile}\n")
        parser.print_help()
        return 1

    menu = create_menu(sections)

    copy_files(header, output_directory_path)

    template = get_template(header['theme']['name'])
    html_out = template.render(
        opla_version=__version__,
        sections=sections,
        header=header,
        menu=menu,
        output=output_directory_path,
        color=header["theme"].get("color"),
    )

    with open(output_directory_path / "index.html", "w") as f:
        f.write(html_out)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
