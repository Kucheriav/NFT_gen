from zoneinfo import ZoneInfo


def to_user_tz(dt, tz_name="Europe/Moscow"):
    # dt — naive datetime в UTC
    if hasattr(dt, "tzinfo") and dt.tzinfo is not None:
        utc_dt = dt
    else:
        utc_dt = dt.replace(tzinfo=ZoneInfo("UTC"))
    return utc_dt.astimezone(ZoneInfo(tz_name))