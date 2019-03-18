import datetime as dt

from notabanane.common.templatetags.common_duration_tags import duration


def test_duration_filter_works_as_expected():
    assert duration(dt.timedelta(minutes=40)) == '40 minutes'
    assert duration(dt.timedelta(hours=1)) == '1 hour'
