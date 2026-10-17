from typing import Union, Dict, List, Any, Optional
from urllib.parse import parse_qs, urlparse, ParseResult
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from Models.Streaming.ChannelManager import Channel
from Errors.ExtractioErrors import StreamUnavailable, StreamResolutionError, DownloadError
from Data.ResolvedStream import Resolved_Stream
from Models.Logger import Extractio_Logger


class YouTubeLiveStream:
    """
    Extract a combined audio/video URL from a YouTube live stream without downloading the stream data.

    Properties:
        __socket_timeout (float): The timeout for socket operations when extracting stream information.
        __logger (Extractio_Logger): The logger instance for extraction-related messages.
    """
    __socket_timeout: float
    """
    The timeout for socket operations when extracting stream information.
    """
    __logger: Extractio_Logger
    """
    The logger instance for extraction-related messages.
    """
    __youtube_downloader: YoutubeDL
    """
    The YoutubeDL instance used for extracting stream information.
    """

    def __init__(
        self,
        socket_timeout: float = 15.0
    ):
        self.setSocketTimeout(socket_timeout)
        self.setLogger(Extractio_Logger("YouTube_LiveStream"))
        self.setYoutubeDownloader(YoutubeDL())

    def getLogger(self) -> Extractio_Logger:
        return self.__logger

    def setLogger(self, logger: Extractio_Logger):
        self.__logger = logger

    def getSocketTimeout(self) -> float:
        return self.__socket_timeout

    def setSocketTimeout(self, socket_timeout: float):
        self.__socket_timeout = socket_timeout

    def getYoutubeDownloader(self) -> YoutubeDL:
        return self.__youtube_downloader

    def setYoutubeDownloader(self, youtube_downloader: YoutubeDL):
        self.__youtube_downloader = youtube_downloader

    def __getLiveInformation(self, current_info: Dict[str, Any], live_info: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Determining the appropriate live information based on the current info and existing live info.

        Procedures:
            1. Return None immediately if there is no existing live information.
            2. Check if the current info type is allowed and if it represents a live stream.
            3. Update the live information with the current info if it is a live stream and the type is not allowed.
            4. Return the final live information, which may be updated or unchanged.

        Parameters:
            current_info (Dict[str, Any]): The current YouTube info dictionary.
            live_info (Optional[Dict[str, Any]]): The existing live information, if any.

        Returns:
            Optional[Dict[str, Any]]: The updated live information, or None if not available.
        """
        if live_info is None:
            return None
        allowed_types: List[str] = [
            "playlist",
            "multi_video"
        ]
        has_live_information: bool = live_info is not None
        has_allowed_type: bool = current_info.get("_type") in allowed_types
        is_live: bool = current_info.get("live_status") == "is_live"
        if (has_live_information and not has_allowed_type and is_live):
            live_info = current_info
        return live_info

    def __extractInfo(self, current_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Extracting detailed information about the current live stream from the provided YouTube info dictionary.

        Procedures:
            1. Check if the current info type is allowed.
            2. Use the current information directly when it is already a live video, otherwise find the live stream entry in its entries list.
            3. Return the detailed information when formats are already present; otherwise extract the selected entry's URL.

        Parameters:
            current_info (Dict[str, Any]): The YouTube info dictionary containing stream details.

        Returns:
            Optional[Dict[str, Any]]: The extracted stream information if available, otherwise None.

        Raises:
            StreamUnavailable: If the current info type is not allowed and there is no live broadcast.
        """
        self.__validateCurrentInfo(current_info)
        entries: List[Dict[str, Any]] = current_info.get("entries") or [] # type: ignore
        live_info: Optional[Dict[str, Any]] = self.__getLiveInformation(current_info, next((item for item in entries if item and item.get("live_status") == "is_live"), None))
        if live_info is None:
            message: str = "The channel is not currently broadcasting."
            self.getLogger().error(message)
            raise StreamUnavailable(message)
        has_formats: bool = bool(live_info.get("formats"))
        has_direct_media_url: bool = isinstance(live_info.get("url"), str)
        has_video_codec: bool = live_info.get("vcodec") not in (None, "none")
        has_audio_codec: bool = live_info.get("acodec") not in (None, "none")
        is_streamable: bool = has_formats or (has_direct_media_url and has_video_codec and has_audio_codec)
        if is_streamable:
            return live_info
        uniform_resource_locator: Optional[str] = (live_info.get("webpage_url") or live_info.get("original_url") or live_info.get("url"))
        if not uniform_resource_locator:
            message = "The live broadcast URL is unavailable."
            self.getLogger().error(message)
            raise StreamUnavailable(message)
        return self.getYoutubeDownloader().extract_info(
            uniform_resource_locator,
            download=False
        ) # type: ignore

    def __validateCurrentInfo(self, current_info: Dict[str, Any]) -> None:
        """
        Validating the current YouTube info dictionary to ensure it is of an allowed type.

        Procedures:
            1. Check if the current info type is in the list of allowed types.
            2. If the type is not allowed but the stream is live, log a warning and return.
            3. If the type is not allowed and the stream is not live, raise a `StreamUnavailable` exception.

        Parameters:
            current_info (Dict[str, Any]): The YouTube info dictionary containing stream details.

        Returns:
            None: This method does not return any value.

        Raises:
            StreamUnavailable: If there is no live broadcast currently available for the channel.
        """
        allowed_types: List[str] = [
            "playlist",
            "multi_video",
        ]
        type: str = str(current_info.get("_type"))
        is_allowed: bool = type in allowed_types
        if is_allowed:
            return
        message: str = "The current information type is not allowed."
        self.getLogger().warn(message)
        if current_info.get("live_status") == "is_live":
            self.getLogger().warn("The current information type is not allowed, but the stream is live.")
            return
        raise StreamUnavailable(message)

    def _extractInfo(self, channel: Channel) -> Dict[str, Any]:
        """
        Extracting the live stream information for the given channel.

        Procedures:
            1. Use YoutubeDL to extract basic information about the channel's live stream.
            2. Check if the extracted information is available.
            3. Use the internal __extractInfo method to get detailed live stream information.
            4. Verify the live status of the stream.
            5. Return the extracted live stream information if available.

        Parameters:
            channel (Channel): The channel for which to extract live stream information.

        Returns:
            Dict[str, Any]: The extracted live stream information.

        Raises:
            StreamUnavailable: If there is no live broadcast currently available for the channel.
        """
        info: Optional[Dict[str, Any]] = self.getYoutubeDownloader().extract_info(channel.youtube_url, download=False) # type: ignore
        if not info:
            message = "There is no live broadcast that is currently available for this channel."
            self.getLogger().error(f"{message} - Name: {channel.display_name} - Uniform Resource Locator: {channel.youtube_url}")
            raise StreamUnavailable(message)
        info = self.__extractInfo(info)
        allowed_statuses: List[str] = [
            "is_upcoming",
            "was_live",
            "not_live",
        ]
        if not info or info.get("live_status") in allowed_statuses:
            message: str = "The channel is not currently broadcasting."
            self.getLogger().error(f"{message} - Name: {channel.display_name} - Uniform Resource Locator: {channel.youtube_url}")
            raise StreamUnavailable(message)
        return info

    def __validateMediaStream(self, candidate: Dict[str, Any]) -> None:
        """
        Validating the media stream candidate to ensure it has a combined audio/video stream.

        Procedures:
            1. Validate the combined media stream.
            2. Validate the remuxing media stream.

        Parameters:
            candidate (Dict[str, Any]): The media stream candidate to validate.

        Returns:
            None: Raises an error if the media stream candidate is not valid.

        Raises:
            StreamUnavailable: If the media stream candidate is not valid, either due to not being a combined stream or remuxing not being enabled.
        """
        self.__validateCombinedMediaStream(candidate)
        self.__validateRemuxingMediaStream(candidate)

    def __validateRemuxingMediaStream(self, candidate: Dict[str, Any]) -> None:
        """
        Validating the remuxing media stream to ensure remuxing is enabled.

        Procedures:
            1. Check if the candidate has requested formats.
            2. Raise an error if remuxing is not enabled.

        Parameters:
            candidate (Dict[str, Any]): The media stream candidate to validate.

        Returns:
            None: Raises an error if remuxing is not enabled.

        Raises:
            StreamUnavailable: If remuxing is not enabled.
        """
        if not candidate.get("requested_formats"):
            return
        message = "Remuxing is not enabled."
        self.getLogger().error(message)
        raise StreamUnavailable(message)

    def __validateCombinedMediaStream(self, candidate: Dict[str, Any]) -> None:
        """
        Validating the combined media stream to ensure it has both video and audio codecs.

        Procedures:
            1. Check if the candidate has both video and audio codecs.
            2. Determine if the candidate is a combined stream.
            3. Raise an error if the stream is not combined.

        Parameters:
            candidate (Dict[str, Any]): The media stream candidate to validate.

        Returns:
            None: Raises an error if the media stream candidate is not a combined stream.

        Raises:
            StreamUnavailable: If the media stream candidate is not a combined stream.
        """
        has_video_codec: bool = candidate.get("vcodec") not in (None, "none")
        has_audio_codec: bool = candidate.get("acodec") not in (None, "none")
        has_combined_stream: bool = has_video_codec and has_audio_codec
        if has_combined_stream:
            return
        message: str = "YouTube did not provide a combined audio/video stream; separate audio/video streams are unsupported."
        self.getLogger().error(message)
        raise StreamUnavailable(message)

    def __validateMediaUniformResourceLocator(
        self,
        candidate: Dict[str, Any],
        formats: List[Dict[str, Any]],
        uniform_resource_locator: Optional[str],
        candidates: List[Dict[str, Any]]
    ) -> None:
        """
        Validating the media uniform resource locator (URL) for the given media stream candidate.

        Procedures:
            1. Validate the media stream candidate to ensure it has a combined audio/video stream.
            2. Check if the provided uniform resource locator (URL) is valid.
            3. If the URL is not valid, determine if there is a valid combined stream.
            4. Raise an error if the URL is not valid and no valid combined stream is available.

        Parameters:
            candidate (Dict[str, Any]): The media stream candidate to validate.
            formats (List[Dict[str, Any]]): The list of available media formats.
            uniform_resource_locator (Optional[str]): The media uniform resource locator (URL) to validate.
            candidates (List[Dict[str, Any]]): The list of candidate media streams.

        Returns:
            None

        Raises:
            StreamUnavailable: If the media URL is not valid and no valid combined stream is available.
        """
        self.__validateMediaStream(candidate)
        is_valid_uniform_resource_locator: bool = isinstance(uniform_resource_locator, str) and self.allowedMediaUniformResourceLocator(uniform_resource_locator)
        if is_valid_uniform_resource_locator:
            return
        is_valid_stream: bool = formats and not candidates # type: ignore
        message: str = "Remuxing is not enabled." if is_valid_stream else "YouTube did not provide a supported combined stream; separate audio/video streams are unsupported."
        self.getLogger().error(message)
        raise StreamUnavailable(message)

    def __resolve(self, channel: Channel, options: Dict[str, Union[bool, float, int, str]]) -> Resolved_Stream:
        """
        Resolving the best available media stream for the given YouTube channel.

        Procedures:
            1. Extract media stream information for the specified channel.
            2. Filter and sort available media formats to identify valid combined streams.
            3. Select the best candidate stream based on format, codec, and resolution.
            4. Validate the selected media stream's URL.
            5. Determine the expiration timestamp for the selected stream.
            6. Return a resolved stream object containing the URL and expiration timestamp.

        Parameters:
            channel (Channel): The YouTube channel for which to resolve the media stream.
            options (Dict[str, Union[bool, float, int, str]]): The options for configuring the YouTube downloader.

        Returns:
            Resolved_Stream: The resolved media stream containing the URL and expiration timestamp.

        Raises:
            StreamUnavailable: If no valid media stream is available.
        """
        downloader_context: YoutubeDL = YoutubeDL(options) # type: ignore
        self.setYoutubeDownloader(downloader_context.__enter__()) # type: ignore
        try:
            info: Optional[Dict[str, Any]] = self._extractInfo(channel)
            formats: List[Dict[str, Any]] = info.get("formats") or []
            candidates: List[Dict[str, Any]] = [item for item in formats if item.get("url") and item.get("vcodec") not in (None, "none") and item.get("acodec") not in (None, "none")]
            candidates.sort(
                key=lambda item: (
                    str(item.get("ext")) == "mp4",
                    "avc" in str(item.get("vcodec", "")).lower() or "h264" in str(item.get("vcodec", "")).lower(),
                    "mp4a" in str(item.get("acodec", "")).lower() or "aac" in str(item.get("acodec", "")).lower(),
                    float(item.get("height") or 0),
                    ),
                reverse=True
            )
            selected: Dict[str, Any] = candidates[0] if candidates else info
            uniform_resource_locator: Optional[str] = selected.get("url")
            self.__validateMediaUniformResourceLocator(
                selected,
                formats,
                uniform_resource_locator,
                candidates
            )
            expires_at: Optional[float] = self.__getExpiresAt(uniform_resource_locator)
            return Resolved_Stream(
                url=str(uniform_resource_locator),
                mime_type=str(selected.get("http_headers", {}).get("Content-Type") or selected.get("mime_type") or "video/mp4"),
                expires_at=expires_at,
                title=str(info.get("title") or channel.display_name),
            )
        finally:
            self.getYoutubeDownloader().close()

    def __getExpiresAt(self, uniform_resource_locator: Optional[str]) -> Optional[float]:
        """
        Getting the expiration timestamp from the uniform resource locator's query parameters.

        Procedures:
            1. Check if the uniform resource locator is provided.
            2. Parse the query parameters from the URL.
            3. Extract the "expire" parameter and convert it to a float.
            4. Handle any parsing errors and return None if necessary.

        Parameters:
            uniform_resource_locator (Optional[str]): The URL containing the expiration query parameter.

        Returns:
            Optional[float]: The expiration timestamp if available, otherwise None.
        """
        if not uniform_resource_locator:
            message: str = "The uniform resource locator is not found."
            self.getLogger().error(message)
            return None
        try:
            return float(parse_qs(urlparse(uniform_resource_locator).query).get("expire", [""])[0])
        except (TypeError, ValueError) as error:
            self.getLogger().error(f"It has failed to parse the uniform resource locator. - Uniform Resource Locator: {uniform_resource_locator} - Error: {error}")
            return None

    def resolve(self, channel: Channel) -> Resolved_Stream:
        """
        Resolving the live stream URL for the given YouTube channel.

        Procedures:
            1. Extract the live stream information from the YouTube channel URL.
            2. Select the best combined audio/video format.
            3. Return the resolved stream URL.

        Parameters:
            channel (Channel): The YouTube channel for which to resolve the live stream URL.

        Returns:
            Resolved_Stream: The resolved live stream information, including the URL and format details.

        Raises:
            StreamUnavailable: If the live stream is not currently available.
            StreamResolutionError: If there is an error resolving the stream URL.
            DownloadError: If there is an error during the extraction process.
        """
        options: Dict[str, Union[bool, float, int, str]] = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "noplaylist": True,
            "ignore_no_formats_error": True,
            "socket_timeout": self.getSocketTimeout(),
            "retries": 0,
            "extractor_retries": 0,
        }
        try:
            return self.__resolve(channel, options)
        except StreamUnavailable as error:
            message: str = "The live stream is unavailable."
            self.getLogger().error(f"{message} - Error: {error}")
            raise StreamUnavailable(message)
        except (DownloadError, TimeoutError, OSError, ValueError) as error:
            message: str = "YouTube live stream resolution failed due to download or network error."
            self.getLogger().error(f"{message} - Error: {error}")
            raise StreamResolutionError(message)
        except Exception as error:
            message: str = "YouTube live stream resolution failed due to an unexpected error."
            self.getLogger().error(f"{message} - Error: {error}")
            raise StreamResolutionError(message) from error

    def allowedMediaUniformResourceLocator(self, uniform_resource_locator: str) -> bool:
        """
        Checking if the given uniform resource locator (URL) is allowed for media streaming.

        Procedures:
            1. Parse the given URL.
            2. Check if the URL uses HTTPS and has no username or password.
            3. Verify that the port is safe (either None or 443).
            4. Ensure the host is "googlevideo.com" or a subdomain of it.
            5. Return True if all checks pass, otherwise return False.

        Parameters:
            uniform_resource_locator (str): The URL to check.

        Returns:
            bool: True if the URL is allowed, False otherwise.
        """
        parsed: ParseResult = urlparse(uniform_resource_locator)
        host: str = (parsed.hostname or "").lower().rstrip(".")
        try:
            safe_port: bool = parsed.port in (None, 443)
        except ValueError as error:
            message: str = "The uniform resource locator is not secured."
            self.getLogger().error(f"{message} - Error: {error}")
            return False
        return (parsed.scheme == "https" and parsed.username is None and parsed.password is None and safe_port and (host == "googlevideo.com" or host.endswith(".googlevideo.com")))
