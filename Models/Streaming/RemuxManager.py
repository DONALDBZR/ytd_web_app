from os import geteuid
from pathlib import Path
from shutil import rmtree, which
from subprocess import DEVNULL, Popen, TimeoutExpired
from tempfile import gettempdir
from threading import Lock
from time import monotonic, sleep, time
from typing import Dict, Optional, List
from uuid import uuid4
from Data.ResolvedStream import Resolved_Stream
from Data.RemuxSession import Remux_Session
from Errors.ExtractioErrors import RemuxUnavailable
from Models.Logger import Extractio_Logger
from atexit import register


class Remux_Manager:
    """
    Manages live remux sessions using FFmpeg, ensuring that each session runs in a secure, isolated temporary directory.

    Properties:
        __temporary_root_path: The root path for temporary remux session directories.
        __remux_root_path: The root path for persistent remux session directories.
        __maximum_sessions: The maximum number of concurrent remux sessions allowed.
        __ffmpeg_path: The path to the FFmpeg executable.
        __lock: A lock to synchronize access to the remux sessions.
        __sessions: A dictionary mapping session slugs to their corresponding remux sessions.
        __logger: The logger instance for the remux manager.
    """
    __temporary_root_path: Path
    """
    The root path for temporary remux session directories.
    """
    __remux_root_path: Path
    """
    The root path for persistent remux session directories.
    """
    __maximum_sessions: int
    """
    The maximum number of concurrent remux sessions allowed.
    """
    __ffmpeg_path: Optional[str]
    """
    The path to the FFmpeg executable.
    """
    __lock: Lock
    """
    A lock to synchronize access to the remux sessions.
    """
    __sessions: Dict[str, Remux_Session]
    """
    A dictionary mapping session slugs to their corresponding remux sessions.
    """
    __logger: Extractio_Logger
    """
    The logger instance for the remux manager.
    """

    def __init__(
        self,
        cache_root: Path,
        max_sessions: int = 2,
        ffmpeg_path: Optional[str] = None
    ):
        """
        Initializing the remux manager with the specified cache root, maximum sessions, and FFmpeg path.

        Procedures:
            1. Set the temporary root path for remux sessions.
            2. Set the persistent remux root path.
            3. Set the maximum number of concurrent remux sessions.
            4. Set the path to the FFmpeg executable.
            5. Initialize the lock for synchronizing access to remux sessions.
            6. Initialize the dictionary for storing remux sessions.
            7. Initialize the logger for the remux manager.
            8. Register the shutdown procedure to be called at exit.

        Parameters:
            cache_root (Path): The root path for persistent remux session directories.
            max_sessions (int): The maximum number of concurrent remux sessions allowed.
            ffmpeg_path (Optional[str]): The path to the FFmpeg executable. If None, the system's FFmpeg will be used.
        """
        self.setTemporaryRootPath(Path(gettempdir()).resolve())
        self.setRemuxRootPath(cache_root.absolute())
        self.setMaximumSessions(max(1, max_sessions))
        self.setFfmpegPath(ffmpeg_path or which("ffmpeg"))
        self.setLock(Lock())
        self.setSessions({})
        self.setLogger(Extractio_Logger("Remux_Manager"))
        register(self.shutdown)

    def getLogger(self) -> Extractio_Logger:
        return self.__logger

    def setLogger(self, logger: Extractio_Logger) -> None:
        self.__logger = logger

    def getSessions(self) -> Dict[str, Remux_Session]:
        return self.__sessions

    def setSessions(self, sessions: Dict[str, Remux_Session]) -> None:
        self.__sessions = sessions

    def getLock(self) -> Lock:
        return self.__lock

    def setLock(self, lock: Lock) -> None:
        self.__lock = lock

    def getFfmpegPath(self) -> Optional[str]:
        return self.__ffmpeg_path

    def setFfmpegPath(self, ffmpeg_path: Optional[str]) -> None:
        self.__ffmpeg_path = ffmpeg_path

    def getMaximumSessions(self) -> int:
        return self.__maximum_sessions

    def setMaximumSessions(self, max_sessions: int) -> None:
        self.__maximum_sessions = max_sessions

    def getRemuxRootPath(self) -> Path:
        return self.__remux_root_path

    def setRemuxRootPath(self, path: Path) -> None:
        self.__remux_root_path = path

    def getTemporaryRootPath(self) -> Path:
        return self.__temporary_root_path

    def setTemporaryRootPath(self, path: Path) -> None:
        self.__temporary_root_path = path

    def getSessionDirectory(self, slug: str, session_id: str) -> Path:
        """
        Building a contained session path from route-validated identifiers.

        Procedures:
            1. Resolve the remux root path.
            2. Construct the session directory path.
            3. Verify that the session directory is within the remux root and temporary root.
            4. Raise an exception if the path is invalid.
            5. Return the resolved session directory path.

        Parameters:
            slug (str): The slug identifier for the session.
            session_id (str): The unique session ID.

        Returns:
            Path: The resolved path to the session directory.

        Raises:
            RemuxUnavailable: If the constructed session path is invalid.
        """
        remux_root = self.getRemuxRootPath().resolve()
        directory = (remux_root / slug / session_id).resolve()
        is_remux_relative_to_root: bool = remux_root.is_relative_to(self.getTemporaryRootPath().resolve())
        is_directory_relative_to_remux_root: bool = directory.is_relative_to(remux_root)
        is_valid: bool = is_remux_relative_to_root and is_directory_relative_to_remux_root
        if is_valid:
            return directory
        message: str = "The session directory is outside the allowed remux and temporary root paths."
        self.getLogger().error(message)
        raise RemuxUnavailable(message)

    @staticmethod
    def __inputOptions(headers: Dict[str, str]) -> List[str]:
        """
        Generating FFmpeg input options based on HTTP headers.

        Procedures:
            1. Initialize the list of FFmpeg input options with reconnect and timeout settings.
            2. Extract the "User-Agent" and "Referer" headers from the HTTP request.
            3. Append the "User-Agent" and "Referer" options to the FFmpeg input options if they are present.
            4. Return the final list of FFmpeg input options.

        Parameters:
            headers (Dict[str, str]): The HTTP headers from the request.

        Returns:
            List[str]: A list of FFmpeg input options.
        """
        options: List[str] = [
            "-rw_timeout",
            "15000000",
            "-reconnect",
            "1",
            "-reconnect_streamed",
            "1",
            "-reconnect_at_eof",
            "1",
            "-reconnect_on_network_error",
            "1",
            "-reconnect_delay_max",
            "5",
        ]
        options = Remux_Manager.__setOptions(options, headers, "User-Agent")
        options = Remux_Manager.__setOptions(options, headers, "Referer")
        return options

    @staticmethod
    def __setOptions(options: List[str], headers: Dict[str, str], key: str) -> List[str]:
        """
        Generating FFmpeg input options for a specific HTTP header key.

        Procedures:
            1. Retrieve the value of the specified HTTP header key from the headers dictionary.
            2. If the value exists, convert the key to a format suitable for FFmpeg options and append it along with the value to the options list.
            3. Return the updated list of FFmpeg input options.

        Parameters:
            options (List[str]): The current list of FFmpeg input options.
            headers (Dict[str, str]): The HTTP headers from the request.
            key (str): The HTTP header key to add to the FFmpeg input options.

        Returns:
            List[str]: The updated list of FFmpeg input options.
        """
        value: Optional[str] = headers.get(key)
        if value:
            new_key: str = key.lower().replace("-", "_")
            options.extend([
                f"-{new_key}",
                value
            ])
        return options

    def __removeSession(self, session: Remux_Session, slug: str) -> None:
        """
        Removing a remux session by stopping it and removing it from the session list.

        Procedures:
            1. Stops a remux session and cleans up its resources.
            2. Removes the session from the session list using the provided slug.

        Parameters:
            session (Remux_Session): The remux session to remove.
            slug (str): The slug associated with the session.

        Returns:
            None
        """
        self.__stopSession(session)
        self.getSessions().pop(slug, None)

    def __removeExistingSession(self, existing: Optional[Remux_Session], slug: str) -> None:
        """
        Removing an existing remux session if it exists.

        Procedures:
            1. Checks if the existing remux session is not None.
            2. If it exists, removes the session using the provided slug.

        Parameters:
            existing (Optional[Remux_Session]): The existing remux session to remove if it exists.
            slug (str): The slug associated with the session.

        Returns:
            None
        """
        if not existing:
            return
        self.__removeSession(existing, slug)

    def __removeRemuxSessions(self, now: float) -> None:
        """
        Removing all stale remux sessions based on the current time.

        Procedures:
            1. Iterates through all remux sessions.
            2. Checks if each session is stale (process terminated or expired).
            3. Removes stale sessions.

        Parameters:
            now (float): The current time used to determine if a session is stale.

        Returns:
            None
        """
        for old_slug, session in list(self.getSessions().items()):
            is_stale: bool = session.process.poll() is not None or session.expires_at <= now
            if not is_stale:
                continue
            self.__removeSession(session, old_slug)

    def __validateSessions(self) -> None:
        """
        Validating the current remux sessions against the maximum allowed capacity.

        Procedures:
            1. Checks if the number of active remux sessions is below the maximum allowed.
            2. If the capacity is full, logs an error and raises a RemuxUnavailable exception.

        Parameters:
            None

        Returns:
            None

        Raises:
            RemuxUnavailable: If the live remux capacity is full.
        """
        if len(self.getSessions()) < self.getMaximumSessions():
            return
        message: str = "The live remux capacity is full."
        self.getLogger().error(message)
        raise RemuxUnavailable(message)

    def __getRemuxSessionDirectory(self, slug: str, session_id: str) -> Path:
        """
        Retrieving the directory for a specific remux session, ensuring the remux root path is valid and writable.

        Procedures:
            1. Creates the remux root path if it doesn't exist.
            2. Validates the remux root path.
            3. Creates the session-specific directory.
            4. Returns the session directory.

        Parameters:
            slug (str): The slug identifying the remux session.
            session_id (str): The unique session ID for the remux session.

        Returns:
            Path: The path to the session-specific directory.

        Raises:
            RemuxUnavailable: If the remux root path is invalid or not writable.
        """
        try:
            self.getRemuxRootPath().mkdir(
                parents=True,
                exist_ok=True,
                mode=0o700
            )
            self.__validateRemuxRootPath()
            self.getRemuxRootPath().chmod(0o700)
            directory = self.getSessionDirectory(slug, session_id)
            directory.mkdir(
                parents=True,
                mode=0o750
            )
            return directory
        except RemuxUnavailable as error:
            message: str = f"The remux root path is invalid."
            self.getLogger().error(f"{message} - Error: {str(error)}")
            raise RemuxUnavailable(message)
        except OSError as error:
            message: str = "The remux cache is not writable."
            self.getLogger().error(f"{message} - Error: {error}")
            raise RemuxUnavailable(message)

    def __validateRemuxRootPath(self) -> None:
        """
        Validating the remux root path to ensure it is not a symbolic link and is owned by the current user.

        Procedures:
            1. Checks if the remux root path is a symbolic link or not owned by the current user.
            2. If the path is invalid, logs an error and raises a RemuxUnavailable exception.

        Raises:
            RemuxUnavailable: If the remux root path is a symbolic link or not owned by the current user.
        """
        is_symbolic_link: bool = self.getRemuxRootPath().is_symlink()
        is_same_user: bool = self.getRemuxRootPath().stat().st_uid == geteuid()
        is_allowed: bool = not is_symbolic_link and is_same_user
        if is_allowed:
            return
        message: str = "The private remux directory has an unexpected owner or link."
        self.getLogger().error(f"{message} - Path: {self.getRemuxRootPath()}")
        raise RemuxUnavailable(message)

    def _startOrReuse(self, slug: str, stream: Resolved_Stream) -> str:
        """
        Starting a new remux session or reuses an existing one if it is still valid.

        Procedures:
            1. Checks if there is an existing remux session for the given slug and if it is still valid.
            2. If a valid existing session is found, returns its session ID.
            3. If no valid session exists, removes any stale sessions and validates the session directory.
            4. Creates a new remux session directory and prepares the FFmpeg command for remuxing.
            5. Starts the FFmpeg process and returns the new session ID.

        Parameters:
            slug (str): The unique identifier for the session.
            stream (Resolved_Stream): The resolved stream object containing video and audio URLs and headers.

        Returns:
            str: The session ID of the active remux session.

        Raises:
            RemuxUnavailable: If the remux session cannot be started or reused.
        """
        now: float = time()
        expiry: float = stream.expires_at or now + 21600
        existing: Optional[Remux_Session] = self.getSessions().get(slug)
        has_existing: bool = existing is not None
        is_existing_process_not_terminated: bool = existing.process.poll() is None if has_existing else False
        is_not_stale_existing: bool = existing.expires_at > now + 30 if has_existing else False
        if has_existing and is_existing_process_not_terminated and is_not_stale_existing:
            return existing.session_id
        self.__removeExistingSession(existing, slug)
        self.__removeRemuxSessions(now)
        self.__validateSessions()
        session_id = uuid4().hex
        directory: Path = self.__getRemuxSessionDirectory(slug, session_id)
        playlist: Path = directory / "index.m3u8"
        segment_pattern: str = "segment%06d.m4s"
        command: List[Optional[str]] = [
            self.getFfmpegPath(),
            "-nostdin",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            *Remux_Manager.__inputOptions(stream.video_headers),
            "-i",
            stream.video_url,
            *Remux_Manager.__inputOptions(stream.audio_headers),
            "-i",
            stream.audio_url,
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c",
            "copy",
            "-t",
            "21600",
            "-f",
            "hls",
            "-hls_time",
            "4",
            "-hls_list_size",
            "8",
            "-hls_flags",
            "delete_segments+omit_endlist",
            "-hls_segment_type",
            "fmp4",
            "-hls_fmp4_init_filename",
            "init.mp4",
            "-hls_segment_filename",
            segment_pattern,
            "index.m3u8",
        ]
        process: Popen = self.__getProcess(command, directory)
        session: Remux_Session = Remux_Session(
            slug,
            session_id,
            directory,
            process,
            expiry
        )
        self.getSessions()[slug] = session
        return self.__getSessionId(
            process,
            session,
            slug,
            playlist,
            directory,
            session_id
        )

    def __getSessionId(
        self,
        process: Popen,
        session: Remux_Session,
        slug: str,
        playlist: Path,
        directory: Path,
        session_id: str
    ) -> str:
        """
        Retrieving the session ID for a live HLS session, ensuring that the session is active and producing segments.

        Procedures:
            1. Check if the session is stale based on the deadline.
            2. If the session is stale, remove it and raise a RemuxUnavailable exception.
            3. Check if the FFmpeg process has exited prematurely.
            4. If the process has exited, remove the session and raise a RemuxUnavailable exception.
            5. Check if the playlist and segments are available.
            6. If available, return the session ID.
            7. If not available, sleep briefly and recursively retry retrieving the session ID.

        Parameters:
            process (Popen): The FFmpeg process for the live HLS session.
            session (Remux_Session): The current live HLS session object.
            slug (str): The unique identifier for the session.
            playlist (Path): The path to the live HLS playlist file.
            directory (Path): The directory containing the live HLS segments.
            session_id (str): The unique session ID to be retrieved.

        Returns:
            str: The session ID if the session is active and producing segments.

        Raises:
            RemuxUnavailable: If the session is stale or the FFmpeg process exits prematurely, or if the live HLS segments are not produced in time.
        """
        deadline: float = monotonic() + 15
        is_not_stale: bool = monotonic() < deadline
        if not is_not_stale:
            self.__removeSession(session, slug)
            message: str = "FFMpeg did not produce live HLS segments before the startup timeout."
            self.getLogger().error(message)
            raise RemuxUnavailable(message)
        if process.poll() is not None:
            self.__removeSession(session, slug)
            message: str = "FFmpeg exited before producing a live playlist."
            self.getLogger().error(message)
            raise RemuxUnavailable(message)
        if playlist.is_file() and any(directory.glob("segment*.m4s")):
            return session_id
        sleep(0.1)
        return self.__getSessionId(
            process,
            session,
            slug,
            playlist,
            directory,
            session_id
        )

    def __getProcess(self, command: List[Optional[str]], directory: Path) -> Popen:
        """
        Getting a Popen process for the given command and working directory.

        Procedures:
            1. Attempt to start a Popen process with the given command and working directory.
            2. If the process cannot be started, clean up the directory and raise a RemuxUnavailable exception.
            3. Return the Popen process if successfully started.

        Parameters:
            command (List[Optional[str]]): The command to execute with Popen.
            directory (Path): The working directory for the Popen process.

        Returns:
            Popen: The started Popen process.

        Raises:
            RemuxUnavailable: If the process cannot be started.
        """
        try:
            return Popen(
                command, # type: ignore
                cwd=directory,
                stdin=DEVNULL,
                stdout=DEVNULL,
                stderr=DEVNULL,
                close_fds=True
            ) # type: ignore
        except OSError as error:
            rmtree(
                directory,
                ignore_errors=True
            )
            message: str = "FFMpeg could not be started."
            self.getLogger().error(f"{message} - Error: {str(error)}")
            raise RemuxUnavailable(message)

    def startOrReuse(self, slug: str, stream: Resolved_Stream) -> str:
        """
        Starting or reusing a remuxing session for a given stream slug.

        Procedures:
            1. Check if an existing remuxing session for the given slug can be reused.
            2. If not, stop any existing session and clean up expired sessions.
            3. Create a new remuxing session if capacity allows.
            4. Return the session ID of the reused or newly created session.

        Parameters:
            slug (str): The unique identifier for the stream.
            stream (Resolved_Stream): The stream object containing video and audio URLs and expiration information.

        Returns:
            str: The session ID of the reused or newly created remuxing session.

        Raises:
            RuntimeError: If remuxing is unavailable due to FFmpeg not being available or the stream not having separate audio and video URLs.
        """
        self.getLock().acquire()
        try:
            self._validateFfmpegPath()
            self._validateUniformResourceLocators(stream)
            return self._startOrReuse(slug, stream)
        except RemuxUnavailable as error:
            message: str = "Remuxing is unavailable."
            self.getLogger().error(f"{message} - Error: {str(error)}")
            raise RuntimeError(message)
        finally:
            self.getLock().release()

    def _validateUniformResourceLocators(self, stream: Resolved_Stream) -> None:
        """
        Validating that the stream has separate video and audio URLs.

        Procedures:
            1. Check if the stream has both video and audio URLs.
            2. If not, log an error and raise a RemuxUnavailable exception.

        Parameters:
            stream (Resolved_Stream): The stream object containing video and audio URLs.

        Returns:
            None

        Raises:
            RemuxUnavailable: If the stream does not have separate audio and video URLs.
        """
        is_allowed: bool = bool(stream.video_url and stream.audio_url)
        if is_allowed:
            return
        message: str = "A separate live audio/video pair is required for remuxing."
        self.getLogger().error(message)
        raise RemuxUnavailable(message)

    def _validateFfmpegPath(self) -> None:
        """
        Validating that the FFmpeg path is set and available.

        Procedures:
            1. Check if the FFmpeg path is set and available.
            2. If not, log an error and raise a RemuxUnavailable exception.

        Returns:
            None

        Raises:
            RemuxUnavailable: If the FFmpeg path is not set or available.
        """
        is_allowed: bool = bool(self.getFfmpegPath())
        if is_allowed:
            return
        message: str = "FFmpeg is required to play this live stream format."
        self.getLogger().error(message)
        raise RemuxUnavailable(message)

    def __stopSession(self, session: Remux_Session) -> None:
        """
        Stopping a remux session and cleaning up its resources.

        Procedures:
            1. Check if the session process is already terminated. If so, remove the session directory and return.
            2. Terminate the session process.
            3. Wait for the process to exit with a timeout.
            4. If the timeout expires, log an error, kill the process, and wait again.
            5. Remove the session directory.

        Parameters:
            session (Remux_Session): The remux session to stop.

        Returns:
            None
        """
        if session.process.poll() is not None:
            rmtree(
                session.directory,
                ignore_errors=True
            )
            return
        session.process.terminate()
        timeout: int = 3
        try:
            session.process.wait(
                timeout=timeout
            )
        except TimeoutExpired as error:
            self.getLogger().error(f"Timeout expired while stopping session. - Error: {str(error)}")
            session.process.kill()
            session.process.wait(
                timeout=timeout
            )
        rmtree(
            session.directory,
            ignore_errors=True
        )

    def shutdown(self) -> None:
        """
        Shutting down the remux manager by stopping all active sessions and clearing the session list.

        Procedures:
            1. Acquire the lock to ensure thread safety.
            2. Iterate through all active sessions and stop each one.
            3. Clear the session list.
            4. Release the lock.

        Returns:
            None
        """
        self.getLock().acquire()
        try:
            for session in self.getSessions().values():
                self.__stopSession(session)
            self.getSessions().clear()
        finally:
            self.getLock().release()
