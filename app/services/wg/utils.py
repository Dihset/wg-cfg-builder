from jinja2 import Template


def get_file_content(file_name) -> str:
    with open(file_name) as f:
        content = f.read()
        return content.strip()


def get_template_by_path(path: str) -> Template:
    with open(path) as file:
        return Template(file.read(), trim_blocks=True)
