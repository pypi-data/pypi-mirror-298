"""Envers."""
# mypy: disable-error-code="attr-defined"

from __future__ import annotations

from importlib import metadata as importlib_metadata


def get_version() -> str:
    """Return the program version."""
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "0.4.1"  # semantic-release


version = get_version()

__version__ = version
__author__ = "Ivan Ogasawara"
__email__ = "ivan.ogasawara@gmail.com"
