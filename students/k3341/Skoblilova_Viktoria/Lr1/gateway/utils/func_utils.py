"""Общие утилиты: батчи, равные части списка, декоратор retry_async для async-функций."""

import functools
import asyncio
from datetime import datetime, timezone, timedelta


def batch_lengh_generator(step: int, data: list) -> list:
    return (data[x : x + step] for x in range(0, len(data), step))


def equal_split(list_to_split, n_parts) -> tuple:
    k, m = divmod(len(list_to_split), n_parts)
    return (
        list_to_split[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)]
        for i in range(n_parts)
    )


def retry_async(num_attempts):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            for try_index in range(num_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if try_index == num_attempts:
                        raise e
                    print(
                        f"Exception occurred: {e}. Retrying... ({try_index + 1}/{num_attempts})"
                    )
                    await asyncio.sleep(1)

        return wrapper

    return decorator


def dt_now_msk() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=3)
