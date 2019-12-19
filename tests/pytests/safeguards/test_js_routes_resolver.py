from io import StringIO

import pytest
from django.core.management import call_command

from project.settings.base import PROJECT_PATH


class TestJsRoutesResolver:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        self.stdout = StringIO()
        self.stderr = StringIO()
        yield
        self.stdout.close()
        self.stderr.close()

    def test_is_up_to_date(self):
        with open(PROJECT_PATH / 'main' / 'static' / 'js' / 'core' / 'reverseUrl.js') as fd:
            current_js_routes_resolver = fd.read()
        call_command('dump_routes_resolver', format='es6', stdout=self.stdout)
        self.stdout.seek(0)
        assert self.stdout.read() == current_js_routes_resolver
