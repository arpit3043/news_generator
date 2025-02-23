from typing import List, Any
from dotenv import load_dotenv
import os
from src.news_aggregrator.core.exceptions import ConfigurationError


class ConfigManager:
    """Singleton configuration manager with enhanced validation"""

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._initialize()
            self._initialized = True

    def _initialize(self):
        load_dotenv()
        self.config = {
            "NEWS_API_KEY": os.getenv("NEWS_API_KEY"),
            "REDDIT_CLIENT_ID": os.getenv("REDDIT_CLIENT_ID"),
            "REDDIT_CLIENT_SECRET": os.getenv("REDDIT_CLIENT_SECRET"),
            "REDDIT_USER_AGENT": os.getenv("REDDIT_USER_AGENT"),
            "NEWS_API_BASE_URL": os.getenv("NEWS_API_BASE_URL"),
            "CACHE_TTL": int(os.getenv("CACHE_TTL", 300)),
            "CACHE_SIZE": int(os.getenv("CACHE_SIZE", 100)),
            "MAX_THREADS": int(os.getenv("MAX_THREADS", 4)),
            "DEFAULT_TIMEOUT": int(os.getenv("DEFAULT_TIMEOUT", 30)),
        }
        self._validate_config()

    def _validate_config(self):
        required_keys = [
            "NEWS_API_KEY",
            "REDDIT_CLIENT_ID",
            "REDDIT_CLIENT_SECRET",
            "REDDIT_USER_AGENT",
            "NEWS_API_BASE_URL",
        ]
        missing_keys = [key for key in required_keys if not self.config.get(key)]
        if missing_keys:
            raise ConfigurationError(
                f"Missing required configuration keys: {', '.join(missing_keys)}"
            )

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def validate_credentials(self, required_keys: List[str]) -> bool:
        return all(self.config.get(key) for key in required_keys)
