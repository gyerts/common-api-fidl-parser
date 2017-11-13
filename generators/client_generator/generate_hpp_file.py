from jinja2 import Environment, FileSystemLoader
import os
from configurations import settings

# Capture our current directory
THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def generate_file(meta: dict, filename: str, template_name: str):
    # Create the jinja2 environment.
    # Notice the use of trim_blocks, which greatly helps control whitespace.
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)

    all = {
        "meta": meta,
        "settings": settings
    }

    content = j2_env.get_template(template_name).render(all)

    with open(os.path.join("output", filename), "w") as f:
        f.write(content)
