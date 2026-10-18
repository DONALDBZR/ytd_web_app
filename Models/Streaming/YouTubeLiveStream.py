from typing import Union, Dict, List, Any, Optional
from urllib.parse import parse_qs, urlparse, ParseResult
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError as YoutubeDLDownloadError
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
        allowed_types: List[str] = [
            "playlist",
            "multi_video"
        ]
        has_allowed_type: bool = current_info.get("_type") in allowed_types
        is_live: bool = current_info.get("live_status") == "is_live"
        if not has_allowed_type and is_live:
            return current_info
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

    def getChannelMetadata(self, channel: Channel) -> Dict[str, Optional[Union[int, bool]]]:
        """
        Retrieving the metadata for the given channel, including subscriber count, video count, and live status.

        Procedures:
            1. Configure YoutubeDL with the necessary options.
            2. Retrieve the video URLs for a specific channel.
            3. Handle any errors that occur during the extraction process.
            4. Parse the extracted information to retrieve subscriber count, video count, and playlist count.
            5. Return the parsed metadata for the channel.

        Parameters:
            channel (Channel): The channel for which to retrieve metadata.

        Returns:
            Dict[str, Optional[Union[int, bool]]]: The metadata for the channel, including subscriber count, video count, and live status.

        Raises:
            StreamResolutionError: If YouTube returns no channel information.
        """
        options: Dict[str, Union[bool, float, int, str]] = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "noplaylist": True,
            "socket_timeout": self.getSocketTimeout(),
            "retries": 0,
            "extractor_retries": 0,
        }
        self.setYoutubeDownloader(YoutubeDL(options)) # type: ignore
        try:
            videos_info: Dict[str, Any] = self.__getVideosUniformResourceLocators(channel)
        except StreamResolutionError as error:
            self.getYoutubeDownloader().close()
            message: str = "The channel returned no video information."
            self.getLogger().error(f"{message} - Name: {channel.display_name} - Uniform Resource Locator: {channel.youtube_url}")
            raise StreamResolutionError(message)
        finally:
            self.getYoutubeDownloader().close()
        channel_follower_count: Union[int, bool] = videos_info.get("channel_follower_count") # type: ignore
        playlist_count: Union[int, bool] = videos_info.get("playlist_count") # type: ignore
        _playlist_count: Optional[int] = int(playlist_count) if isinstance(playlist_count, int) else None
        channel_video_count: Union[int, bool] = videos_info.get("channel_video_count", _playlist_count)
        video_count: Optional[int] = int(channel_video_count) if isinstance(channel_video_count, int) else None
        subscriber_count: Optional[int] = int(channel_follower_count) if isinstance(channel_follower_count, int) else None
        return {
            "subscriber_count": subscriber_count,
            "video_count": video_count,
            "is_live": self.__getIsLive(channel),
        }

    def __getIsLive(self, channel: Channel) -> bool:
        """
        Determining whether a specific channel is currently live.

        Procedures:
            1. Retrieve the live stream information for a specific channel.
            2. Determine the live status based on the retrieved information.

        Parameters:
            channel (Channel): The channel to check for live status.

        Returns:
            bool: True if the channel is live, False otherwise.
        """
        try:
            live_info: Optional[Dict[str, Any]] = self.__getLiveInformationData(channel)
            return False if not live_info else str(live_info.get("live_status")) == "live"
        except YoutubeDLDownloadError as error:
            message: str = "The live status lookup failed."
            self.getLogger().warn(f"{message} - Error: {str(error)}")
            return False

    def __getLiveInformationData(self, channel: Channel) -> Optional[Dict[str, Any]]:
        """
        Retrieving the live stream information for a specific channel.

        Procedures:
            1. Use the configured YoutubeDL instance to extract information about the channel's live stream.
            2. Return the extracted live stream information.

        Parameters:
            channel (Channel): The channel for which to retrieve live stream information.

        Returns:
            Optional[Dict[str, Any]]: The extracted live stream information, or None if extraction fails.
        """
        return self.getYoutubeDownloader().extract_info(
            channel.youtube_url,
            download=False
        ) # type: ignore

    def __getVideosUniformResourceLocators(self, channel: Channel) -> Dict[str, Any]:
        """
        Retrieving the video URLs for a specific channel.

        Procedures:
            1. Use the configured YoutubeDL instance to extract information about the channel's videos.
            2. Return the extracted video information.

        Parameters:
            channel (Channel): The channel for which to retrieve video URLs.

        Returns:
            Dict[str, Any]: The extracted video information.

        Raises:
            StreamResolutionError: If the video information cannot be retrieved.
        """
        videos_info: Optional[Dict[str, Any]] = self.getYoutubeDownloader().extract_info(
            f"{channel.youtube_url.rsplit('/', 1)[0]}/videos",
            download=False
        ) # type: ignore
        if not videos_info:
            message = "YouTube returned no channel statistics."
            self.getLogger().error(f"{message} - Name: {channel.display_name} - Uniform Resource Locator: {channel.youtube_url}")
            raise StreamResolutionError(message)
        return videos_info

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
            requested_formats: List[Dict[str, Any]] = info.get("requested_formats") or []
            format_options: List[Dict[str, Any]] = requested_formats + formats
            candidates: List[Dict[str, Any]] = [item for item in format_options if item.get("url") and item.get("vcodec") not in (None, "none") and item.get("acodec") not in (None, "none")]
            if (info.get("url") and info.get("vcodec") not in (None, "none") and info.get("acodec") not in (None, "none") and not requested_formats):
                candidates.append(info)
            candidates.sort(
                key=lambda item: (
                    str(item.get("ext")) == "mp4",
                    "avc" in str(item.get("vcodec", "")).lower() or "h264" in str(item.get("vcodec", "")).lower(),
                    "mp4a" in str(item.get("acodec", "")).lower() or "aac" in str(item.get("acodec", "")).lower(),
                    float(item.get("height") or 0),
                    ),
                reverse=True
            )
            if candidates:
                selected: Dict[str, Any] = candidates[0]
                uniform_resource_locator: Optional[str] = selected.get("url")
                self.__validateMediaUniformResourceLocator(
                    selected,
                    format_options,
                    uniform_resource_locator,
                    candidates
                )
                expires_at: Optional[float] = self.__getExpiresAt(uniform_resource_locator)
                return Resolved_Stream(
                    url=str(uniform_resource_locator),
                    mime_type=str(selected.get("http_headers", {}).get("Content-Type") or selected.get("mime_type") or "video/mp4"),
                    expires_at=expires_at,
                    title=str(info.get("title") or channel.display_name)
                )
            video_formats: List[Dict[str, Any]] = [item for item in format_options if item.get("url") and item.get("vcodec") not in (None, "none") and item.get("acodec") in (None, "none")]
            audio_formats: List[Dict[str, Any]] = [item for item in format_options if item.get("url") and item.get("acodec") not in (None, "none") and item.get("vcodec") in (None, "none")]
            video_formats.sort(
                key=lambda item: (
                    "avc" in str(item.get("vcodec", "")).lower() or "h264" in str(item.get("vcodec", "")).lower(),
                    float(item.get("height") or 0),
                    float(item.get("tbr") or 0),
                ),
                reverse=True
            )
            audio_formats.sort(
                key=lambda item: (
                    "mp4a" in str(item.get("acodec", "")).lower() or "aac" in str(item.get("acodec", "")).lower(),
                    float(item.get("abr") or item.get("tbr") or 0),
                ),
                reverse=True
            )
            if not video_formats or not audio_formats:
                message: str = "YouTube did not provide a compatible live audio/video format pair."
                self.getLogger().error(message)
                raise StreamUnavailable(message)
            video: Dict[str, Any] = video_formats[0]
            audio: Dict[str, Any] = audio_formats[0]
            video_url: str = str(video.get("url") or "")
            audio_url: str = str(audio.get("url") or "")
            if not self.allowedMediaUniformResourceLocator(video_url) or not self.allowedMediaUniformResourceLocator(audio_url):
                message: str = "YouTube returned a media URL outside the allowed CDN hosts."
                self.getLogger().error(message)
                raise StreamUnavailable(message)
            expires = [
                expiry for expiry in (self.__getExpiresAt(video_url), self.__getExpiresAt(audio_url))
                if expiry is not None
            ]
            return Resolved_Stream(
                url="",
                mime_type="application/vnd.apple.mpegurl",
                expires_at=min(expires) if expires else None,
                title=str(info.get("title") or channel.display_name),
                video_url=video_url,
                audio_url=audio_url,
                video_headers=self.__safeMediaHeaders(video.get("http_headers")),
                audio_headers=self.__safeMediaHeaders(audio.get("http_headers")),
            )
        finally:
            self.getYoutubeDownloader().close()

    def __safeMediaHeaders(self, value: Any) -> Dict[str, str]:
        """
        Safely extracting non-sensitive HTTP headers from the provided value.

        Procedures:
            1. Check if the value is a dictionary.
            2. Extract only the "User-Agent" and "Referer" headers.
            3. Ensure the header values do not contain carriage return or newline characters.
            4. Return the safe headers as a dictionary.

        Parameters:
            value (Any): The input value that may contain HTTP headers.

        Returns:
            Dict[str, str]: A dictionary containing only the safe HTTP headers.
        """
        if not isinstance(value, dict):
            return {}
        safe_headers: Dict[str, str] = {}
        allowed_keys: List[str] = [
            "User-Agent",
            "Referer"
        ]
        for key in allowed_keys:
            header_value = value.get(key)
            is_string: bool = isinstance(header_value, str)
            has_cariage: bool = "\r" in str(header_value)
            has_newline: bool = "\n" in str(header_value)
            is_allowed: bool = is_string and not has_cariage and not has_newline
            if not is_allowed:
                continue
            safe_headers[str(key)] = header_value # type: ignore
        return safe_headers

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
        except (YoutubeDLDownloadError, DownloadError, TimeoutError, OSError, ValueError) as error:
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
