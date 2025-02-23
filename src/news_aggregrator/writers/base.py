from abc import ABC, abstractmethod
from typing import List
from src.news_aggregrator.core.models import Article


class ContentWriter(ABC):
    """Abstract base class for content writers"""

    @abstractmethod
    def write(self, articles: List[Article]) -> None:
        """Abstract method to write a list of articles"""
        pass
