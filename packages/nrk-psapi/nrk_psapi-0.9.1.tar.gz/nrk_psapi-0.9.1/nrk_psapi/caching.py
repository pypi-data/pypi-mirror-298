from __future__ import annotations

import asyncio
import contextlib
from functools import lru_cache, partial
import os
from typing import Callable

import cloudpickle
from diskcache import Cache, Disk
from diskcache.core import ENOVAL, UNKNOWN, args_to_key, full_name
from platformdirs import user_cache_dir

from .const import DISK_CACHE_DURATION, LOGGER as _LOGGER

_caching_enabled = True


class CloudpickleDisk(Disk):  # pragma: no cover
    def __init__(self, directory, compress_level=1, **kwargs):
        self.compress_level = compress_level
        super().__init__(directory, **kwargs)

    def put(self, key):
        data = cloudpickle.dumps(key)
        return super().put(data)

    def get(self, key, raw):
        data = super().get(key, raw)
        return cloudpickle.loads(data)

    def store(self, value, read, key=UNKNOWN):
        if not read:
            value = cloudpickle.dumps(value)
        return super().store(value, read, key=key)

    def fetch(self, mode, filename, value, read):
        data = super().fetch(mode, filename, value, read)
        if not read:
            data = cloudpickle.loads(data)
        return data


@lru_cache(1)
def get_cache():
    """Get the context object that contains previously-computed return values."""
    cache_dir = os.environ.get("NRK_PSAPI_CACHE_DIR", None)
    _LOGGER.debug(f"get_cache(): {cache_dir}")
    if cache_dir is None:  # pragma: no cover
        cache_dir = user_cache_dir("nrk-psapi", ensure_exists=True)
    return Cache(
        cache_dir,
        eviction_policy="none",
        cull_limit=0,
        disk=CloudpickleDisk,
    )


# noinspection PyUnusedLocal
def cache(expire: float | None = DISK_CACHE_DURATION, typed=False, ignore=()):
    """Cache decorator for memoizing function calls."""

    def decorator(cached_function: Callable):
        memory = get_cache()

        base = (full_name(cached_function),)

        if asyncio.iscoroutinefunction(cached_function):

            async def wrapper(*args, **kwargs):  # noqa: ANN002 # pragma: no cover
                if not _caching_enabled:
                    return await cached_function(*args, **kwargs)
                cache_key = wrapper.__cache_key__(*args, **kwargs)
                loop = asyncio.get_running_loop()
                result = await loop.run_in_executor(
                    None,
                    partial(
                        wrapper.__memory__.get,
                        key=cache_key,
                        default=ENOVAL,
                        retry=True,
                    ),
                )

                if result is ENOVAL:
                    result = await cached_function(*args, **kwargs)
                    await loop.run_in_executor(
                        None,
                        partial(
                            wrapper.__memory__.set,
                            key=cache_key,
                            value=result,
                            expire=expire,
                            retry=True,
                        ),
                    )

                return result

        else:  # pragma: no cover

            def wrapper(*args, **kwargs):  # noqa: ANN002
                if not _caching_enabled:
                    return cached_function(*args, **kwargs)

                cache_key = wrapper.__cache_key__(*args, **kwargs)
                result = wrapper.__memory__.get(cache_key, default=ENOVAL, retry=True)

                if result is ENOVAL:
                    result = cached_function(*args, **kwargs)
                    wrapper.__memory__.set(cache_key, result, expire, retry=True)

                return result

        def __cache_key__(*args, **kwargs):  # noqa: N807, ANN002  # pragma: no cover
            """Make key for cache given function arguments."""
            return args_to_key(base, args, kwargs, typed, ignore)

        wrapper.__cache_key__ = __cache_key__
        wrapper.__memory__ = memory
        wrapper.__wrapped__ = cached_function

        return wrapper

    return decorator


def disable_cache():
    """Disable the cache for this session."""
    global _caching_enabled  # noqa: PLW0603
    _caching_enabled = False


def clear_cache():  # pragma: no cover
    """Erase the cache completely."""
    memory = get_cache()
    memory.clear()


@contextlib.contextmanager
def cache_disabled():  # pragma: no cover
    global _caching_enabled  # noqa: PLW0603
    original_state = _caching_enabled
    _caching_enabled = False
    try:
        yield
    finally:
        _caching_enabled = original_state
