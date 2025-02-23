import sys
import logging
from src.news_aggregrator.config.config_manager import ConfigManager
from src.news_aggregrator.core.exceptions import NewsAggregatorError
from src.news_aggregrator.fetchers.news_api import NewsAPIFetcher
from src.news_aggregrator.services.aggregrator import NewsContentAggregator
from src.news_aggregrator.writers.file_writer import FileWriter

logger = logging.getLogger(__name__)  # Set up logger for error handling


def main():
    """Main function to fetch, aggregate, and write news articles"""
    try:
        config = ConfigManager()  # Load configuration settings
        fetchers = [NewsAPIFetcher()]  # Initialize news fetchers
        aggregator = NewsContentAggregator(fetchers)  # Create aggregator instance

        topics = ["startup", "entrepreneurship", "techology", "unicorn"]  # Define topics to fetch

        articles = aggregator.fetch_all_content(topics)  # Fetch and aggregate articles

        file_writer = FileWriter("news_results.json")  # Initialize file writer
        file_writer.write(articles)  # Save articles to JSON file

    except NewsAggregatorError as e:
        logger.error(f"Application error: {str(e)}")  # Log application-specific errors
        sys.exit(1)  # Exit with error status

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")  # Log unexpected errors
        sys.exit(1)  # Exit with error status


if __name__ == "__main__":
    main()  # Run the script
