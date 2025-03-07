class CrawlerNotAllowedError(Exception):
    """The Crawler is not allowed to crawl."""
    pass

class NotFoundError(Exception):
    """The file is not found externally."""

class DownloadError(Exception):
    """The download has failed."""