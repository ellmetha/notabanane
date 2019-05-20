"""
    Common context managers
    =======================

    This module exposes common context managers.

"""

import contextlib
from typing import Generator

from django.utils import translation


@contextlib.contextmanager
def switch_language(language: str) -> Generator:
    """ A context manager to easily switch to another language. """
    current_lang = translation.get_language()
    translation.activate(language)
    yield
    translation.activate(current_lang)  # type: ignore
