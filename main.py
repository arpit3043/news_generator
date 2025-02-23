import sys
import logging
from src.news_aggregrator.config.config_manager import ConfigManager
from src.news_aggregrator.core.exceptions import NewsAggregatorError
from src.news_aggregrator.fetchers.news_api import NewsAPIFetcher
from src.news_aggregrator.services.aggregrator import NewsContentAggregator
from src.news_aggregrator.writers.file_writer import FileWriter

logger = logging.getLogger(__name__)


def main():
    try:
        config = ConfigManager()
        fetchers = [NewsAPIFetcher()]
        aggregator = NewsContentAggregator(fetchers)
        topics = ["startup", "entrepreneurship", "techology", "unicorn"]

        articles = aggregator.fetch_all_content(topics)

        file_writer = FileWriter("news_results.json")
        file_writer.write(articles)

    except NewsAggregatorError as e:
        logger.error(f"Application error: {str(e)}")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
