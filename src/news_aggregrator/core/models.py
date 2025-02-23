from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class Article:
    """Represents a news article with metadata"""

    title: str
    url: Optional[str] = None
    source: Optional[str] = None
    published_at: Optional[datetime] = None
    topic: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Converts published_at to a datetime object if it's a string"""
        if self.published_at and isinstance(self.published_at, str):
            self.published_at = datetime.fromisoformat(
                self.published_at.replace("Z", "+00:00")
            )
