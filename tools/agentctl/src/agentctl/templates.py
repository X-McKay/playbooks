"""Load scaffold text from installed package resources."""

from importlib.resources import files
from string import Template


def render_template(template_name: str, **values: object) -> str:
    return Template(
        files("agentctl")
        .joinpath("templates", template_name)
        .read_text(encoding="utf-8")
    ).substitute(values)
