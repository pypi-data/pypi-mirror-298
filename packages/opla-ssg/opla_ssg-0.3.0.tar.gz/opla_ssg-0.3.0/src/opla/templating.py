"""Provide a function to get the jinja template."""

from pathlib import Path

import jinja2

from . import THEMES

TEMPLATES_PATH = Path(__file__).parent / "themes"


def get_template(theme: str) -> jinja2.Template:
    """
    Get the appropriate template according to the theme name

    Args:
        theme: the theme name

    Returns:
        jinja2.Template: the requested template
    """

    if theme not in THEMES:
        raise ValueError(f"Unknown theme name: '{theme}'")

    base_loader = jinja2.FileSystemLoader(TEMPLATES_PATH / "base" / "templates")
    theme_loader = jinja2.FileSystemLoader(TEMPLATES_PATH / theme / "templates")

    env = jinja2.Environment(loader=jinja2.ChoiceLoader([theme_loader, base_loader]))
    template = env.get_template("index.html.j2")

    return template
