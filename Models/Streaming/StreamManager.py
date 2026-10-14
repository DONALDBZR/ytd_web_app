from threading import BoundedSemaphore, Lock
from time import monotonic, time
from typing import Dict, Tuple, Optional
from Models.Streaming.ChannelManager import Channel, ChannelManager
from Models.Streaming.YouTubeLiveStream import Resolved_Stream, StreamUnavailable, YouTubeLiveStream
from Errors.ExtractioErrors import ResolutionBusy
from Models.Logger import Extractio_Logger


class Stream_Manager:
    """
    Coordinates bounded stream resolution and short-lived URL caching for YouTube live streams.

    Attributes:
        __channels: Manages the registration and retrieval of YouTube streaming channels.
        __resolver: Handles the resolution of YouTube live streams.
        __ttl: Time-to-live for cached stream resolutions.
        __slots: Controls the maximum number of concurrent stream resolutions.
        __lock: Ensures thread-safe access to the cache and failure records.
        __cache: Stores cached stream resolutions along with their expiration times.
        __failures: Tracks recent resolution failures to prevent immediate retries.
        __logger: Handles logging for the Stream Manager.
    """
    __channels: ChannelManager
    """
    Manages the registration and retrieval of YouTube streaming channels.
    """
    __resolver: YouTubeLiveStream
    """
    Handles the resolution of YouTube live streams.
    """
    __ttl: int
    """
    Time-to-live for cached stream resolutions.
    """
    __slots: BoundedSemaphore
    """
    Controls the maximum number of concurrent stream resolutions.
    """
    __lock: Lock
    """
    Ensures thread-safe access to the cache and failure records.
    """
    __cache: Dict[str, Tuple[float, Resolved_Stream]]
    """
    Stores cached stream resolutions along with their expiration times.
    """
    __failures: Dict[str, float]
    """
    Tracks recent resolution failures to prevent immediate retries.
    """
    __logger: Extractio_Logger
    """
    Handles logging for the Stream Manager.
    """

    def __init__(
        self,
        channels: ChannelManager,
        resolver: YouTubeLiveStream,
        cache_ttl: int = 20,
        max_concurrent: int = 2
    ):
        self.setChannels(channels)
        self.setResolver(resolver)
        self.setTTL(max(0, cache_ttl))
        self.setSlots(BoundedSemaphore(max(1, max_concurrent)))
        self.setLock(Lock())
        self.setCache({})
        self.setFailures({})
        self.setLogger(Extractio_Logger("Stream_Manager"))

    def getLogger(self) -> Extractio_Logger:
        return self.__logger

    def setLogger(self, logger: Extractio_Logger) -> None:
        self.__logger = logger

    def getFailures(self) -> Dict[str, float]:
        return self.__failures

    def setFailures(self, failures: Dict[str, float]) -> None:
        self.__failures = failures

    def getCache(self) -> Dict[str, Tuple[float, Resolved_Stream]]:
        return self.__cache

    def setCache(self, cache: Dict[str, Tuple[float, Resolved_Stream]]) -> None:
        self.__cache = cache

    def getSlots(self) -> BoundedSemaphore:
        return self.__slots

    def setSlots(self, slots: BoundedSemaphore) -> None:
        self.__slots = slots

    def getLock(self) -> Lock:
        return self.__lock

    def setLock(self, lock: Lock) -> None:
        self.__lock = lock

    def getResolver(self) -> YouTubeLiveStream:
        return self.__resolver

    def getTTL(self) -> int:
        return self.__ttl

    def setTTL(self, ttl: int) -> None:
        self.__ttl = max(0, ttl)

    def setResolver(self, resolver: YouTubeLiveStream) -> None:
        self.__resolver = resolver

    def getChannels(self) -> ChannelManager:
        return self.__channels

    def setChannels(self, channels: ChannelManager) -> None:
        self.__channels = channels

    def __getCached(self, channel: Channel) -> Optional[Resolved_Stream]:
        """
        Retrieving the cached stream for the given channel if it exists and is still valid.

        Procedures:
            1. Check if there is a cached stream for the channel.
            2. If a cached stream exists, check if it is still valid based on its expiration time.
            3. If the cached stream is valid, return it.
            4. If the cached stream has expired, check if there have been recent resolution failures.
            5. If there are recent failures, raise a RuntimeError.
            6. If there are no recent failures, return None.

        Parameters:
            channel (Channel): The channel for which to retrieve the cached stream.

        Returns:
            Optional[Resolved_Stream]: The cached stream if it exists and is valid, otherwise None.

        Raises:
            RuntimeError: If there was a recent resolution failure.
        """
        now: float = monotonic()
        cached: Optional[Tuple[float, Resolved_Stream]] = self.getCache().get(channel.slug)
        if not cached:
            return None
        (expiry_at, stream) = cached
        if expiry_at > now:
            return stream
        has_failures: bool = self.getFailures().get(channel.slug, 0) > now
        if not has_failures:
            return None
        raise RuntimeError("Recent resolution failed; retry shortly")

    def __acquireSlot(self) -> None:
        """
        Attempting to acquire a slot for stream resolution.

        Returns:
            None: If a slot is successfully acquired.

        Raises:
            ResolutionBusy: If no slots are available for stream resolution.
        """
        if self.getSlots().acquire(blocking=False):
            return
        message: str = "No available slots for stream resolution."
        self.getLogger().error(message)
        raise ResolutionBusy(message)

    def __manageCache(self, channel: Channel, stream: Resolved_Stream) -> None:
        """
        Managing the caching of a resolved stream for a given channel.

        Procedures:
            1. Check if the TTL (time-to-live) is set.
            2. If TTL is set, store the stream in the cache with an expiry time.
            3. If TTL is not set, remove the stream from the cache.

        Parameters:
            channel (Channel): The channel for which to manage the cache.
            stream (Resolved_Stream): The resolved stream to be cached.

        Returns:
            None: This method does not return any value.
        """
        if self.getTTL():
            self.getCache()[channel.slug] = (monotonic() + self.getTTL(), stream)
        else:
            self.getCache().pop(channel.slug, None)

    def __resolveStream(self, channel: Channel) -> Optional[Resolved_Stream]:
        """
        Resolving the stream for a given channel.

        Procedures:
            1. Attempt to resolve the stream using the resolver.
            2. If successful, manage the cache and return the resolved stream.
            3. If the stream is unavailable, log the error and raise a RuntimeError.
            4. If any other error occurs, log the error, update failures, and raise a RuntimeError.
            5. Release the acquired slot regardless of the outcome.

        Parameters:
            channel (Channel): The channel for which to resolve the stream.

        Returns:
            Optional[Resolved_Stream]: The resolved stream if successful, otherwise None.

        Raises:
            RuntimeError: If the stream cannot be resolved.
            StreamUnavailable: If the stream is unavailable.
        """
        try:
            stream: Resolved_Stream = self.getResolver().resolve(channel)
            self.setTTL(self.getTTL() if stream.expires_at is None else min(self.getTTL(), max(0, int(stream.expires_at - time()))))
            self.__manageCache(channel, stream)
            self.getFailures().pop(channel.slug, None)
            return stream
        except StreamUnavailable as error:
            message: str = "The stream is unavailable."
            self.getLogger().error(f"{message} - Error: {error}")
            self.getCache().pop(channel.slug, None)
            self.getFailures().pop(channel.slug, None)
            raise RuntimeError(message)
        except Exception as error:
            message: str = f"An error occurred during stream resolution"
            self.getLogger().error(f"{message} - Error: {error}")
            self.getCache().pop(channel.slug, None)
            self.getFailures()[channel.slug] = monotonic() + 10
            raise RuntimeError(message)
        finally:
            self.getSlots().release()

    def __validateStream(self, stream: Optional[Resolved_Stream]) -> Resolved_Stream:
        """
        Validating the resolved stream.

        Procedures:
            1. Check if the stream is not None.
            2. If the stream is None, log an error and raise a RuntimeError.

        Parameters:
            stream (Optional[Resolved_Stream]): The stream to validate.

        Returns:
            Resolved_Stream: The validated stream if it is not None.

        Raises:
            RuntimeError: If the stream is None.
        """
        if stream is not None:
            return stream
        message: str = "The stream is invalid."
        self.getLogger().error(message)
        raise RuntimeError(message)

    def resolve(self, channel: Channel) -> Resolved_Stream:
        """
        Resolving the stream for the given channel.

        Procedures:
            1. Acquire the lock for thread safety.
            2. Attempt to retrieve the cached stream.
            3. Acquire a resolution slot.
            4. Resolve the stream if it is not cached.
            5. Validate the resolved stream.
            6. Handle any runtime errors or resolution busy errors.

        Parameters:
            channel (Channel): The channel for which to resolve the stream.

        Returns:
            Resolved_Stream: The resolved and validated stream.

        Raises:
            RuntimeError: If the stream cannot be resolved or if no resolution slot is available.
        """
        self.getLock().acquire(blocking=True)
        try:
            stream: Optional[Resolved_Stream] = self.__getCached(channel)
            self.__acquireSlot()
            stream = stream if stream is not None else self.__resolveStream(channel)
            return self.__validateStream(stream)
        except RuntimeError as error:
            self.getLock().release()
            message: str = "The stream cannot be retrieved due to that recent resolution failure."
            self.getLogger().error(f"{message} - Error: {error}")
            raise RuntimeError(message)
        except ResolutionBusy as error:
            self.getLock().release()
            message: str = "There is no available slot for stream resolution."
            self.getLogger().error(f"{message} - Error: {error}")
            raise RuntimeError(message)
        finally:
            self.getLock().release()

    def invalidate(self, slug: str) -> None:
        """
        Invalidating the cache for the given slug.

        Procedures:
            1. Acquire the lock for thread safety.
            2. Remove the cache entry for the given slug.
            3. Remove the failure entry for the given slug.
            4. Release the lock after the invalidation attempt.

        Parameters:
            slug (str): The slug for which to invalidate the cache.

        Returns:
            None
        """
        self.getLock().acquire(blocking=True)
        try:
            self.getCache().pop(slug, None)
            self.getFailures().pop(slug, None)
        finally:
            self.getLock().release()
