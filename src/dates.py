"""Date helpers.

Digest filenames and titles use the local calendar date (respects the TZ
environment variable, e.g. TZ=Asia/Taipei in docker-compose), never UTC:
a run at 07:00 Taipei is still "today", not yesterday's UTC date.
"""

from datetime import datetime
from typing import Optional


def local_date_str(now: Optional[datetime] = None) -> str:
    """Return the local date as YYYY-MM-DD.

    `now` may be an aware datetime (converted to local time) and defaults
    to the current time.
    """
    dt = now.astimezone() if now else datetime.now().astimezone()
    return dt.strftime("%Y-%m-%d")
