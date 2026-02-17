from importlib.metadata import PackageNotFoundError, version


def get_version() -> str:
    try:
        return version("bussdcc-system-health")
    except PackageNotFoundError:
        return "0.0.0"


__version__ = get_version()
