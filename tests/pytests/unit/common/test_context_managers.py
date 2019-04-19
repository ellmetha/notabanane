from django.test import override_settings
from django.utils.translation import get_language

from notabanane.common.context_managers import switch_language


@override_settings(LANGUAGES=[('en', 'English'), ('fr', 'French')])
def test_switch_language_allows_to_switch_language():
    with switch_language('en'):
        assert get_language() == 'en'
    with switch_language('fr'):
        assert get_language() == 'fr'
