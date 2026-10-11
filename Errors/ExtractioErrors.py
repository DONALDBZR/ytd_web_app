class CrawlerNotAllowedError(Exception):
    """The Crawler is not allowed to crawl."""
    pass

class NotFoundError(Exception):
    """The file is not found externally."""
    pass

class DownloadError(Exception):
    """The download has failed."""
    pass

class ForgedRequestError(Exception):
    """The request is forged."""
    pass

class ChannelConfigurationError(ValueError):
    """Raised when a channel entry is invalid."""
    pass