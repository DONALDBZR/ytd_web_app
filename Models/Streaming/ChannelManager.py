from typing import Dict, Iterable, List, Optional, Pattern
from urllib.parse import urlparse
from Errors.ExtractioErrors import ChannelConfigurationError
from re import compile, fullmatch
from Data.StreamingChannel import Channel
from Models.Logger import Extractio_Logger
from json import loads, JSONDecodeError


class Channel_Manager:
    """
    Manages the registration and retrieval of YouTube streaming channels.

    Attributes:
        __channels (Dict[str, Channel]): A dictionary mapping channel slugs to Channel objects.
        __logger (Extractio_Logger): Logger instance for the Extractio application.
        __slug_pattern (Pattern[str]): Compiled regular expression pattern for validating YouTube channel slugs.
        __channel_id_pattern (Pattern[str]): Compiled regular expression pattern for validating YouTube channel IDs.
        __handle_pattern (Pattern[str]): Compiled regular expression pattern for validating YouTube channel handles.
    """
    __channels: Dict[str, Channel]
    """
    Manages the registration and retrieval of YouTube streaming channels.
    """
    __logger: Extractio_Logger
    """
    This class manages a logger instance for the Extractio application.
    """
    __slug_pattern: Pattern[str]
    """
    This class manages a compiled regular expression pattern for validating YouTube channel slugs.
    """
    __channel_id_pattern: Pattern[str]
    """
    This class manages a compiled regular expression pattern for validating YouTube channel IDs.
    """
    __handle_pattern: Pattern[str]
    """
    This class manages a compiled regular expression pattern for validating YouTube channel handles.
    """

    def __init__(self, entries: Optional[Iterable[dict]] = None):
        """
        Initializing the ChannelManager with optional channel entries.

        Procedures:
            1. Initialize the internal channels dictionary.
            2. Initialize the logger instance.
            3. Register each provided channel entry, ensuring the maximum limit is not exceeded.

        Parameters:
            entries (Optional[Iterable[dict]]): An optional iterable of channel entries to register.

        Raises:
            ChannelConfigurationError: If the maximum number of channels is exceeded.
        """
        self.setChannels({})
        self.setLogger(Extractio_Logger("Channel_Manager"))
        self.setSlugPattern(compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$"))
        self.setChannelIdPattern(compile(r"^UC[a-zA-Z0-9_-]{22}$"))
        self.setHandlePattern(compile(r"^@[a-zA-Z0-9._-]{3,30}$"))
        if entries is None:
            self.getLogger().inform("No channel entries provided")
            return
        for entry in entries:
            if len(self.getChannels()) < 256:
                self.register(entry)
                continue
            message = "Maximum number of channels reached"
            self.getLogger().error(message)
            raise ChannelConfigurationError(message)

    def getChannels(self) -> Dict[str, Channel]:
        return self.__channels.copy()

    def setChannels(self, channels: Dict[str, Channel]) -> None:
        self.__channels = channels.copy()

    def getLogger(self) -> Extractio_Logger:
        return self.__logger

    def setLogger(self, logger: Extractio_Logger) -> None:
        self.__logger = logger

    def getSlugPattern(self) -> Pattern[str]:
        return self.__slug_pattern

    def setSlugPattern(self, slug_pattern: Pattern[str]) -> None:
        self.__slug_pattern = slug_pattern

    def getHandlePattern(self) -> Pattern[str]:
        return self.__handle_pattern

    def setHandlePattern(self, handle_pattern: Pattern[str]) -> None:
        self.__handle_pattern = handle_pattern

    def getChannelIdPattern(self) -> Pattern[str]:
        return self.__channel_id_pattern

    def setChannelIdPattern(self, channel_id_pattern: Pattern[str]) -> None:
        self.__channel_id_pattern = channel_id_pattern

    def canonicalChannelUrl(self, value: str) -> str:
        """
        Converting a YouTube channel URL, handle, or UC channel ID into a canonical live URL.

        Procedures:
            1. Strip leading and trailing whitespace from the input value.
            2. Match the value against known patterns for UC channel IDs, handles, and slugs.
            3. Construct and return the canonical live URL based on the matched pattern.
            4. Raise ChannelConfigurationError if the value does not match any known pattern.

        Parameters:
            value (str): The YouTube channel URL, handle, or UC channel ID to convert.

        Returns:
            str: The canonical live URL for the given YouTube channel.

        Raises:
            ChannelConfigurationError: If the input value does not match any known pattern.
        """
        value = value.strip()
        if self.getChannelIdPattern().fullmatch(value):
            self.getLogger().inform("Matched channel ID pattern")
            return f"https://www.youtube.com/channel/{value}/live"
        if self.getHandlePattern().fullmatch(value):
            self.getLogger().inform("Matched handle pattern")
            return f"https://www.youtube.com/{value}/live"
        parsed = urlparse(value if "://" in value else f"https://{value}")
        host = (parsed.hostname or "").lower().rstrip(".")
        allowed_hosts = {
            "youtube.com",
            "www.youtube.com",
            "m.youtube.com"
        }
        if parsed.scheme != "https" or host not in allowed_hosts:
            message = "Only secure hosts are supported for YouTube channels."
            self.getLogger().error(f"{message} - Uniform Resource Locator: {value}")
            raise ChannelConfigurationError(message)
        match = fullmatch(r"/(@[A-Za-z0-9._-]{3,30}|channel/UC[A-Za-z0-9_-]{22})(?:/(?:live|streams|videos))?/?", parsed.path)
        if not match:
            message = "Failed to match YouTube channel URL pattern."
            self.getLogger().error(f"{message} - Uniform Resource Locator: {value}")
            raise ChannelConfigurationError(message)
        identity = match.group(1)
        self.getLogger().inform(f"The channel has been identified.  - Channel: {identity}")
        return f"https://www.youtube.com/{identity}/live"

    @classmethod
    def fromJson(cls, configuration: str) -> "Channel_Manager":
        """
        Creating a ChannelManager instance from a JSON configuration string.

        Procedures:
            1. Strip the input configuration string.
            2. If the configuration is empty, return a default ChannelManager instance.
            3. Parse the JSON string into a list of channel entries.
            4. Validate that the parsed data is a list.
            5. Initialize a ChannelManager instance with the parsed entries.
            6. Return the initialized ChannelManager instance.

        Parameters:
            configuration (str): A JSON string representing the channel configuration.

        Returns:
            Channel_Manager: An instance of Channel_Manager initialized with the parsed channels.

        Raises:
            ChannelConfigurationError: If the configuration is not a valid JSON array or contains invalid entries.
        """
        if not configuration.strip():
            return cls()
        try:
            entries = loads(configuration)
        except (TypeError, JSONDecodeError) as error:
            message = "The streaming channels has an invalid JSON format."
            cls().getLogger().error(f"{message} - Error: {error}")
            raise ChannelConfigurationError(message)
        if not isinstance(entries, list):
            message = "The streaming channels has an invalid JSON format."
            cls().getLogger().error(message)
            raise ChannelConfigurationError(message)
        return cls(entries)

    def register(self, entry: Dict[str, str]) -> Channel:
        """
        Registering a new channel with the ChannelManager.

        Procedures:
            1. Validate the input entry.
            2. Ensure the channel slug is unique and within limits.
            3. Validate the display name, URL, and enabled status.
            4. Create a Channel instance and add it to the manager.
            5. Return the created Channel instance.

        Parameters:
            entry (Dict[str, str]): A dictionary containing channel information.

        Returns:
            Channel: The created Channel instance.

        Raises:
            ChannelConfigurationError: If the entry is invalid or violates constraints.
        """
        if not isinstance(entry, dict):
            message = "The channel is in an invalid format."
            self.getLogger().error(message)
            raise ChannelConfigurationError(message)
        slug = entry.get("slug")
        name = entry.get("display_name")
        uniform_resource_locator = entry.get("url")
        enabled = entry.get("enabled", True)
        if not isinstance(slug, str) or not self.getSlugPattern().fullmatch(slug):
            message = "The channel slug is invalid."
            self.getLogger().error(f"{message} - Slug: {slug}")
            raise ChannelConfigurationError(message)
        if slug in self.getChannels():
            message = "The channel slug must be unique."
            self.getLogger().error(f"{message} - Slug: {slug}")
            raise ChannelConfigurationError(message)
        if len(self.getChannels()) >= 256:
            message = "The maximum number of channels has been reached."
            self.getLogger().error(message)
            raise ChannelConfigurationError(message)
        if not isinstance(name, str) or not name.strip() or len(name) > 120:
            message = "The channel name is required."
            self.getLogger().error(f"{message} - Name: {name}")
            raise ChannelConfigurationError(message)
        if not isinstance(uniform_resource_locator, str):
            message = "The uniform resource locator for the channel is required."
            self.getLogger().error(f"{message} - Uniform Resource Locator: {uniform_resource_locator}")
            raise ChannelConfigurationError(message)
        if not isinstance(enabled, bool):
            message = "The channel must have been enabled."
            self.getLogger().error(message)
            raise ChannelConfigurationError(message)
        channel = Channel(
            slug,
            name.strip(),
            self.canonicalChannelUrl(uniform_resource_locator),
            enabled
        )
        current_channels: Dict[str, Channel] = self.getChannels()
        current_channels[slug] = channel
        self.setChannels(current_channels)
        return channel

    def get(self, slug: str) -> Optional[Channel]:
        return self.getChannels().get(slug)

    def list(self, enabled_only: bool = False) -> List[Channel]:
        return [channel for channel in self.getChannels().values() if channel.enabled or not enabled_only]
