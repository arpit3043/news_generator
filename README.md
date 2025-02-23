## News Generator

The News Generator is a Python-based project that fetches the latest news headlines related to technology, startups, and entrepreneurship. The project leverages the NewsAPI to retrieve relevant articles and provides a modular structure with support for caching, retry logic, and pluggable fetchers and writers.

## Table of Contents

- [Features](#features)
- [Directory Structure](#directory-structure)
- [Setup and Installation](#setup-and-installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Modular Architecture:** Easily integrate multiple fetchers and writers.
- **Caching:** Uses TTLCache to cache API responses.
- **Retry Decorator:** Automatically retries failed fetch requests.
- **Configuration Management:** Centralized configuration management using environment variables.
- **Detailed Logging:** Logs errors and retry attempts for better troubleshooting.

## Directory Structure

```News Generator
.
├── src
│   └── content_aggregator
│       ├── config
│       │   └── config_manager.py
│       ├── core
│       │   ├── exceptions.py
│       │   └── models.py
│       ├── fetchers
│       │   ├── base.py
│       │   └── news_api.py
│       ├── services
│       │   └── aggregator.py
│       ├── utils
│       │   └── decorators.py
│       └── writers
│           ├── base.py
│           └── file_writer.py
└── main.py
└── requirements.txt
