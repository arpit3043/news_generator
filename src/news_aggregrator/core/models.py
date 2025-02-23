from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class Article:
    title: str
    url: Optional[str] = None
    source: Optional[str] = None
    published_at: Optional[datetime] = None
    topic: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.published_at and isinstance(self.published_at, str):
            self.published_at = datetime.fromisoformat(
                self.published_at.replace("Z", "+00:00")
            )
