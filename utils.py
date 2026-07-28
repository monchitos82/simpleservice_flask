from datetime import UTC, datetime


def get_now_time() -> object:
    """Return a timestamp in UTC timezone"""
    return datetime.now(UTC)


def fibonacci(number: int = 0) -> int:
    if not number or number <= 0:
        return 0
    if number == 1:
        return 1
    if number >= 2:
        a, b = 0, 1
        for i in range(1, number):
            a, b = b, a + b
        return b
