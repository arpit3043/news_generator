class NewsAggregatorError(Exception):
    """Base exception for content aggregator"""

    pass


class ConfigurationError(NewsAggregatorError):
    """Raised when there's a configuration error"""

    pass


class FetcherError(NewsAggregatorError):
    """Raised when there's an error fetching content"""

    pass


class WriterError(NewsAggregatorError):
    """Raised when there's an error writing content"""

    pass
