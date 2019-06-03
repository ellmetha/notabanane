import datetime as dt

from main.common.templatetags.common_duration_tags import duration, iso8601


def test_duration_filter_works_as_expected():
    assert duration(dt.timedelta(minutes=40)).replace('\xa0', ' ') == '40 minutes'
    assert duration(dt.timedelta(hours=1)).replace('\xa0', ' ') == '1 heure'


def test_iso8601_filter_works_as_expected():
    assert iso8601(dt.timedelta(minutes=40)) == 'PT40M'
    assert iso8601(dt.timedelta(hours=1)) == 'PT1H'
