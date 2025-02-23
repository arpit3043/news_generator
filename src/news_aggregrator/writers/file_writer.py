from typing import List
import json
from src.news_aggregrator.core.models import Article
from src.news_aggregrator.core.exceptions import WriterError
from src.news_aggregrator.writers.base import ContentWriter


class FileWriter(ContentWriter):
    """Writes articles to a JSON file"""

    def __init__(self, filename: str):
        """Initializes the file writer with a filename"""
        self.filename = filename

    def write(self, articles: List[Article]) -> None:
        """Writes a list of articles to a file in JSON format"""
        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(
                    [self._article_to_dict(article) for article in articles],  # Convert articles to dict
                    file,
                    indent=2,
                    default=str,  # Ensure non-serializable objects (like datetime) are converted to strings
                )
        except Exception as e:
            raise WriterError(f"Error writing to file: {str(e)}")  # Handle write errors

    def _article_to_dict(self, article: Article) -> dict:
        """Converts an Article object into a dictionary"""
        return {
            "title": article.title,
            "url": article.url,
            "source": article.source,
            "published_at": (
                article.published_at.isoformat() if article.published_at else None  # Convert datetime to string
            ),
            "topic": article.topic,
            "metadata": article.metadata,
        }
