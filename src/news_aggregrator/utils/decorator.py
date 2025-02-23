import functools
import logging
import time
from typing import Callable, Any
from src.news_aggregrator.core.exceptions import NewsAggregatorError

logger = logging.getLogger(__name__)


def retry(max_attempts: int = 3, delay: int = 1):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(
                        f"Attempt {attempt + 1}/{max_attempts} failed: {str(e)}"
                    )
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
            raise NewsAggregatorError(
                f"Failed after {max_attempts} attempts: {str(last_exception)}"
            )

        return wrapper

    return decorator


def validate_input(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        return func(*args, **kwargs)

    return wrapper
