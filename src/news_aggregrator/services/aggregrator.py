from datetime import datetime
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.news_aggregrator.core.models import Article
from src.news_aggregrator.core.exceptions import NewsAggregatorError
from src.news_aggregrator.fetchers.base import ContentFetcher
from src.news_aggregrator.config.config_manager import ConfigManager


class NewsContentAggregator:
    def __init__(self, fetchers: List[ContentFetcher]):
        self.fetchers = fetchers
        self.config = ConfigManager()
        self.seen_titles = {}
        self.articles_by_topic: Dict[str, List[Article]] = {}

    def fetch_all_content(self, topics: List[str]) -> List[Article]:
        all_articles = []
        max_threads = self.config.get("MAX_THREADS", 4)

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            future_to_task = {
                executor.submit(self._fetch_content, fetcher, topic): (fetcher, topic)
                for fetcher in self.fetchers
                for topic in topics
            }

            for future in as_completed(future_to_task):
                fetcher, topic = future_to_task[future]
                try:
                    articles = future.result()
                    self._process_articles(articles, topic)
                    all_articles.extend(articles)
                except Exception as e:
                    raise NewsAggregatorError(
                        f"Error processing {fetcher.__class__.__name__} "
                        f"results for {topic}: {str(e)}"
                    )

        return sorted(
            all_articles, key=lambda x: x.published_at or datetime.min, reverse=True
        )

    def _fetch_content(self, fetcher: ContentFetcher, topic: str) -> List[Article]:
        return fetcher.fetch(topic)

    def _process_articles(self, articles: List[Article], topic: str) -> None:
        for article in articles:
            if article.title not in self.seen_titles:
                self.seen_titles[article.title] = article
                if topic not in self.articles_by_topic:
                    self.articles_by_topic[topic] = []
                self.articles_by_topic[topic].append(article)
