from jinja2 import Environment, FileSystemLoader
import os
from configurations import settings

j2_env = None
generate_to = None


def set_template_dir(directory: str, generate_to_path: str):
    global j2_env
    global generate_to
    generate_to = generate_to_path
    j2_env = Environment(loader=FileSystemLoader(directory), trim_blocks=True)


def generate_file(meta: dict, filename: str, template_name: str):
    # Create the jinja2 environment.
    # Notice the use of trim_blocks, which greatly helps control whitespace.
    global j2_env
    global generate_to

    all = {
        "meta": meta,
        "settings": settings
    }

    content = j2_env.get_template(template_name).render(all)

    with open(os.path.join(generate_to, filename), "w") as f:
        f.write(content)
