import logging
import time

import httpx

from app.utils.settings import Settings

logger = logging.getLogger(__name__)

_CACHE_TTL = 3600  # 1 hour in seconds

_cached_courses: list[dict] | None = None
_cache_timestamp: float = 0.0

_settings = Settings()


def get_courses() -> list[dict]:
    """
    Fetch courses from R2 storage, returning a cached copy if it is less than
    one hour old. On failure, the stale cache is returned when available.
    """
    global _cached_courses, _cache_timestamp  # noqa: PLW0603

    now = time.monotonic()
    if _cached_courses is not None and (now - _cache_timestamp) < _CACHE_TTL:
        return _cached_courses

    url = f"{_settings.DATA_STORAGE_URL.rstrip('/')}/courses.json"
    try:
        response = httpx.get(url, timeout=30)
        response.raise_for_status()
        _cached_courses = response.json()
        _cache_timestamp = now
        logger.info("Courses refreshed from %s", url)
    except Exception:
        logger.exception("Failed to fetch courses from %s", url)
        if _cached_courses is None:
            raise

    return _cached_courses  # type: ignore[return-value]
