import re

provider_pathregex = re.compile(r"(?:(.+)/)*([\w_]+)$")


def provider_path_partition(path: str):
    g = provider_pathregex.match(path)
    if not g:
        raise ValueError("invalid provider path, should be [anyfilter/]<provider>")
    return g.groups()


def service_fullname(service):
    return f"{service.category}/{service.name}/{str(service.protocol)}"


def read_os_release() -> dict[str, str]:
    text = ""

    for fpath in ("/etc/os-release", "/etc/lib/os-release", "/etc/initrd-release"):
        try:
            with open(fpath) as f:
                text = f.read()
        except Exception:
            pass

    return parse_env(text)


def parse_env(text: str):
    os_release = dict()

    lines = text.splitlines()

    for ln in lines:
        if "=" in ln:
            k, v = ln.split("=")
            os_release[k] = v.strip(' "')

    return os_release


def item_splitpath(path: str):
    name, _, attr = path.partition(".")
    attr, _, _ = attr.partition(".")
    return name, attr


def item_attr(path: str):
    _, p = item_splitpath(path)
    return p


def get_item_type(path: str):
    n, _ = item_splitpath(path)
    return n
