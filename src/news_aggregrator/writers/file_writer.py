from typing import List
import json
from src.news_aggregrator.core.models import Article
from src.news_aggregrator.core.exceptions import WriterError
from src.news_aggregrator.writers.base import ContentWriter


class FileWriter(ContentWriter):
    def __init__(self, filename: str):
        self.filename = filename

    def write(self, articles: List[Article]) -> None:
        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(
                    [self._article_to_dict(article) for article in articles],
                    file,
                    indent=2,
                    default=str,
                )
        except Exception as e:
            raise WriterError(f"Error writing to file: {str(e)}")

    def _article_to_dict(self, article: Article) -> dict:
        return {
            "title": article.title,
            "url": article.url,
            "source": article.source,
            "published_at": (
                article.published_at.isoformat() if article.published_at else None
            ),
            "topic": article.topic,
            "metadata": article.metadata,
        }
