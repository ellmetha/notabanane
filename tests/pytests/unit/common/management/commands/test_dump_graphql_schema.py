import tempfile
from io import StringIO

import pytest
from django.core.management import call_command
from django.utils.translation import activate, get_language
from graphene_django.settings import graphene_settings
from graphql.utilities.print_schema import print_schema


class TestDumpGraphqlSchema:
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

    def test_can_export_the_dump_of_the_graphql_schema_to_the_standard_output(self):
        call_command('dump_graphql_schema', stdout=self.stdout)
        self.stdout.seek(0)
        expected = print_schema(graphene_settings.SCHEMA.graphql_schema).strip()
        assert self.stdout.read().strip() == expected

    def test_can_export_the_dump_of_the_graphql_schema_to_a_single_file(self):
        export_filename = tempfile.mktemp()
        call_command('dump_graphql_schema', output=export_filename, stdout=self.stdout)
        with open(export_filename) as fd:
            assert fd.read() == print_schema(graphene_settings.SCHEMA.graphql_schema)
