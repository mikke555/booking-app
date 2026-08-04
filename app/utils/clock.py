from datetime import UTC, date, datetime


def today() -> date:
    return datetime.now(UTC).date()
