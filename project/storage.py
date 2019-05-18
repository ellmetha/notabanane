"""
    Project base file storages
    ==========================

    This file defines basic file storages that can be used to manage files (uploads, staticfiles)
    in the project.

"""

import os

from django.contrib.staticfiles.storage import ManifestFilesMixin
from storages.backends.s3boto3 import S3Boto3Storage, SpooledTemporaryFile


class CustomS3Boto3Storage(S3Boto3Storage):
    """ Temporary fix for Django storages issue
        https://github.com/jschneier/django-storages/issues/382
    """

    def _save_content(self, obj, content, parameters):
        """
        We create a clone of the content file as when this is passed to boto3 it wrongly closes
        the file upon upload where as the storage backend expects it to still be open
        """
        # Seek our content back to the start
        content.seek(0, os.SEEK_SET)

        # Create a temporary file that will write to disk after a specified size
        content_autoclose = SpooledTemporaryFile()

        # Write our original content into our copy that will be closed by boto3
        content_autoclose.write(content.read())

        # Upload the object which will auto close the content_autoclose instance
        super(CustomS3Boto3Storage, self)._save_content(obj, content_autoclose, parameters)

        # Cleanup if this is fixed upstream our duplicate should always close
        if not content_autoclose.closed:
            content_autoclose.close()


class MediaRootS3BotoStorage(CustomS3Boto3Storage):
    location = 'm'


class StaticRootS3BotoStorage(ManifestFilesMixin, CustomS3Boto3Storage):
    location = 's'
