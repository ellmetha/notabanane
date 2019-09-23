from io import StringIO

import pytest
from django.core.management import call_command

from project.settings.base import PROJECT_PATH


class TestGraphqlSchema:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        self.stdout = StringIO()
        self.stderr = StringIO()
        yield
        self.stdout.close()
        self.stderr.close()

    def test_is_up_to_date(self):
        with open(PROJECT_PATH / 'project' / 'data' / 'graphql_schema.json') as fd:
            current_graphql_schema = fd.read()
        call_command('graphql_schema', out='-', stdout=self.stdout)
        self.stdout.seek(0)
        assert self.stdout.read().strip() == current_graphql_schema.strip()
