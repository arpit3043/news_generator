from abc import ABC, abstractmethod
from typing import List, Optional
from src.news_aggregrator.core.models import Article
from cachetools import TTLCache
from src.news_aggregrator.config.config_manager import ConfigManager


class ContentFetcher(ABC):
    """Abstract base class for content fetchers with caching"""

    def __init__(self):
        """Initializes the fetcher with a config manager and cache"""
        self.config = ConfigManager()  # Load configuration settings
        self.cache = TTLCache(
            maxsize=self.config.get("CACHE_SIZE", 100),  # Max cache size
            ttl=self.config.get("CACHE_TTL", 300),  # Time-to-live for cache items
        )

    @abstractmethod
    def fetch(self, query: str) -> List[Article]:
        """Abstract method to fetch articles based on a query"""
        pass

    def get_cached_results(self, query: str) -> Optional[List[Article]]:
        """Retrieves cached results for a given query if available"""
        return self.cache.get(query)

    def cache_results(self, query: str, articles: List[Article]):
        """Stores fetched articles in the cache for future use"""
        self.cache[query] = articles
