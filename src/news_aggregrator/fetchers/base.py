from abc import ABC, abstractmethod
from typing import List, Optional
from src.news_aggregrator.core.models import Article
from cachetools import TTLCache
from src.news_aggregrator.config.config_manager import ConfigManager


class ContentFetcher(ABC):
    """Abstract base class for content fetchers with caching"""

    def __init__(self):
        self.config = ConfigManager()
        self.cache = TTLCache(
            maxsize=self.config.get("CACHE_SIZE", 100),
            ttl=self.config.get("CACHE_TTL", 300),
        )

    @abstractmethod
    def fetch(self, query: str) -> List[Article]:
        pass

    def get_cached_results(self, query: str) -> Optional[List[Article]]:
        return self.cache.get(query)

    def cache_results(self, query: str, articles: List[Article]):
        self.cache[query] = articles
