import os
import time
from datetime import datetime, timezone

import pytest

from src.dates import local_date_str


@pytest.fixture
def taipei_tz():
    prev = os.environ.get("TZ")
    os.environ["TZ"] = "Asia/Taipei"
    time.tzset()
    yield
    if prev is None:
        os.environ.pop("TZ", None)
    else:
        os.environ["TZ"] = prev
    time.tzset()


def test_late_utc_evening_is_next_day_locally(taipei_tz):
    # 2026-07-13 07:21 Taipei == 2026-07-12 23:21 UTC; the digest must be
    # dated 07-13, not 07-12 (the bug that overwrote yesterday's post).
    utc_now = datetime(2026, 7, 12, 23, 21, tzinfo=timezone.utc)
    assert local_date_str(utc_now) == "2026-07-13"


def test_same_calendar_day(taipei_tz):
    utc_now = datetime(2026, 7, 13, 4, 0, tzinfo=timezone.utc)  # 12:00 Taipei
    assert local_date_str(utc_now) == "2026-07-13"


def test_defaults_to_current_time(taipei_tz):
    expected = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d")
    assert local_date_str() == expected
