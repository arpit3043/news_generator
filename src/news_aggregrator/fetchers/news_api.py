import requests
from typing import List
from src.news_aggregrator.core.models import Article
from src.news_aggregrator.core.exceptions import FetcherError
from src.news_aggregrator.fetchers.base import ContentFetcher
from src.news_aggregrator.utils.decorator import retry


class NewsAPIFetcher(ContentFetcher):
    """Fetcher for retrieving news articles from NewsAPI"""

    def __init__(self):
        """Initializes the fetcher with API credentials and base URL"""
        super().__init__()
        self.api_key = self.config.get("NEWS_API_KEY")  # API key for authentication
        self.base_url = self.config.get("NEWS_API_BASE_URL")  # Base URL for NewsAPI
        self._validate_credentials()  # Ensure credentials are present

    def _validate_credentials(self):
        """Validates that the API key is available"""
        if not self.api_key:
            raise FetcherError("NewsAPI credentials missing")

    @retry(max_attempts=3)
    def fetch(self, query: str) -> List[Article]:
        """Fetches news articles for a given query, with caching"""
        cached_results = self.get_cached_results(query)
        if cached_results:
            return cached_results  # Return cached results if available

        try:
            params = {
                "q": query,  # Search query
                "sortBy": "publishedAt",  # Sort by latest published date
                "language": "en",  # Fetch English news articles
                "apiKey": self.api_key,  # API key for authentication
            }
            response = requests.get(
                self.base_url, params=params, timeout=self.config.get("DEFAULT_TIMEOUT")
            )
            response.raise_for_status()  # Raise an error for HTTP issues

            articles = [
                self._create_article(article_data, query)
                for article_data in response.json().get("articles", [])
            ]
            self.cache_results(query, articles)  # Cache fetched articles
            return articles
        except requests.exceptions.RequestException as e:
            raise FetcherError(f"Error fetching news for '{query}': {str(e)}")

    def _create_article(self, article_data: dict, query: str) -> Article:
        """Creates an Article object from NewsAPI response data"""
        return Article(
            title=article_data["title"],
            url=article_data["url"],
            source="NewsAPI",
            published_at=article_data["publishedAt"],
            topic=query,  # Store query as topic for categorization
            metadata={
                "author": article_data.get("author"),
                "description": article_data.get("description"),
            },
        )
