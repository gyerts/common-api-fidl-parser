from jinja2 import Environment, FileSystemLoader
import os
from configurations import settings

j2_env = None


def set_template_dir(directory: str):
    global j2_env
    j2_env = Environment(loader=FileSystemLoader(directory), trim_blocks=True)


def generate_file(meta: dict, filename: str, template_name: str):
    # Create the jinja2 environment.
    # Notice the use of trim_blocks, which greatly helps control whitespace.
    global j2_env

    all = {
        "meta": meta,
        "settings": settings
    }

    content = j2_env.get_template(template_name).render(all)

    with open(os.path.join("output", filename), "w") as f:
        f.write(content)
