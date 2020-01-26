from main.common.cache import constants as c
from main.common.cache.context_processors import constants


def test_constants_returns_the_expected_constants():
    assert constants({}) == {
        'TINY_TTL': c.TINY_TTL,
        'SHORT_TTL': c.SHORT_TTL,
        'MIDDLE_TTL': c.MIDDLE_TTL,
        'LONG_TTL': c.MIDDLE_TTL,
        'FOREVER_TTL': c.FOREVER_TTL,
    }
