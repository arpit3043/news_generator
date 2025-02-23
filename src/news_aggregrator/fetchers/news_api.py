import requests
from typing import List
from src.news_aggregrator.core.models import Article
from src.news_aggregrator.core.exceptions import FetcherError
from src.news_aggregrator.fetchers.base import ContentFetcher
from src.news_aggregrator.utils.decorator import retry


class NewsAPIFetcher(ContentFetcher):
    def __init__(self):
        super().__init__()
        self.api_key = self.config.get("NEWS_API_KEY")
        self.base_url = self.config.get("NEWS_API_BASE_URL")
        self._validate_credentials()

    def _validate_credentials(self):
        if not self.api_key:
            raise FetcherError("NewsAPI credentials missing")

    @retry(max_attempts=3)
    def fetch(self, query: str) -> List[Article]:
        cached_results = self.get_cached_results(query)
        if cached_results:
            return cached_results

        try:
            params = {
                "q": query,
                "sortBy": "publishedAt",
                "language": "en",
                "apiKey": self.api_key,
            }
            response = requests.get(
                self.base_url, params=params, timeout=self.config.get("DEFAULT_TIMEOUT")
            )
            response.raise_for_status()

            articles = [
                self._create_article(article_data, query)
                for article_data in response.json().get("articles", [])
            ]
            self.cache_results(query, articles)
            return articles
        except requests.exceptions.RequestException as e:
            raise FetcherError(f"Error fetching news for '{query}': {str(e)}")

    def _create_article(self, article_data: dict, query: str) -> Article:
        return Article(
            title=article_data["title"],
            url=article_data["url"],
            source="NewsAPI",
            published_at=article_data["publishedAt"],
            topic=query,
            metadata={
                "author": article_data.get("author"),
                "description": article_data.get("description"),
            },
        )
