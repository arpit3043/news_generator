import functools
import logging
import time
from typing import Callable, Any
from src.news_aggregrator.core.exceptions import NewsAggregatorError

logger = logging.getLogger(__name__)


def retry(max_attempts: int = 3, delay: int = 1):
    """Decorator to retry a function in case of failure"""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)  # Try executing the function
                except Exception as e:
                    last_exception = e
                    logger.warning(
                        f"Attempt {attempt + 1}/{max_attempts} failed: {str(e)}"
                    )  # Log failure
                    if attempt < max_attempts - 1:
                        time.sleep(delay)  # Wait before retrying
            raise NewsAggregatorError(
                f"Failed after {max_attempts} attempts: {str(last_exception)}"
            )  # Raise exception after max attempts

        return wrapper

    return decorator


def validate_input(func: Callable) -> Callable:
    """Placeholder decorator for input validation"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        return func(*args, **kwargs)  # Currently does nothing, can be expanded

    return wrapper
