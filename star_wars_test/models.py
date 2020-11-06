import uuid
from pathlib import Path

import petl as etl
from django.conf import settings
from django.db import models

from .petl_html_display import display_html
from .sw_controller import Fetcher, PeopleManager

# Create your models here.
BASE_FETCH_PATH = Path("fetch/")


def get_file_path(file_name):
    # concatenate different paths and add the filename to generate the final file path
    return settings.MEDIA_ROOT / BASE_FETCH_PATH / file_name


class PeopleFetchManager(models.Manager):
    people_manager = PeopleManager()

    def fetch(self):
        fetcher = Fetcher()
        data = fetcher.get_data()
        table = self.people_manager.get_clean_table(data)
        # sort the table headers
        etl.sortheader(table)
        file_name = "{}.csv".format(uuid.uuid4())
        file_path = get_file_path(file_name)
        # save the table as CSV on disk
        etl.tocsv(table, file_path)
        return self.create(file_name=file_name)


class PeopleFetch(models.Model):
    file_name = models.CharField(max_length=255, unique=True)
    fetching_date = models.DateTimeField(auto_now_add=True)
    objects = PeopleFetchManager()  # New default manager

    def __str__(self):
        return self.file_name

    @property
    def file_path(self):
        return get_file_path(self.file_name)

    def get_html_etl_table(self, limit=10):
        return display_html(self.get_etl_table(), limit=limit, )

    def get_etl_table(self):
        return etl.fromcsv(self.file_path)
