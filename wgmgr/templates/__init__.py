import jinja2

environment = jinja2.Environment(loader=jinja2.PackageLoader("wgmgr", "templates"))


def get_template(name: str) -> jinja2.Template:
    return environment.get_template(name)
