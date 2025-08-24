from dataclasses import dataclass


@dataclass
class YouTube_Get_By_Channel:
    """
    A dataclass representing a YouTube video record for `YouTube.getByChannel()`.
    """
    identifier: str
    duration: str
    channel: str
    title: str
    uniform_resource_locator: str
    media_identifier: int