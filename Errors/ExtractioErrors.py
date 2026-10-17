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

class StreamUnavailable(Exception):
    """The channel has no playable public live broadcast."""
    pass

class StreamResolutionError(Exception):
    """YouTube could not be resolved at this time."""
    pass

class ResolutionBusy(Exception):
    """All configured resolver slots are occupied."""
    pass

class RemuxUnavailable(RuntimeError):
    """Raised when a separate-track live stream cannot be remuxed."""
    pass