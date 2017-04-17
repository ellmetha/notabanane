# -*- coding: utf-8 -*-

import os
import shutil

import pytest

from . import settings


@pytest.yield_fixture(scope='session', autouse=True)
def empty_media():
    """ Removes the files in MEDIA_ROOT that could have been created during tests execution. """
    yield
    if os.path.exists(settings.MEDIA_ROOT):
        for candidate in os.listdir(settings.MEDIA_ROOT):
            path = os.path.join(settings.MEDIA_ROOT, candidate)
            try:
                shutil.rmtree(path)
            except OSError:
                os.remove(path)
