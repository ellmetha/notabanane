from io import StringIO

import pytest
from django.core.management import call_command
from django.utils.translation import activate, get_language

from project.settings.base import PROJECT_PATH


class TestGraphqlSchema:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        current_locale = get_language()
        activate('fr')
        self.stdout = StringIO()
        self.stderr = StringIO()
        yield
        self.stdout.close()
        self.stderr.close()
        activate(current_locale)

    def test_is_up_to_date(self):
        with open(PROJECT_PATH / 'project' / 'db' / 'schema.graphql') as fd:
            current_graphql_schema = fd.read()
        call_command('dump_graphql_schema', stdout=self.stdout)
        self.stdout.seek(0)
        assert self.stdout.read().strip() == current_graphql_schema.strip()
