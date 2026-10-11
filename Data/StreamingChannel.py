from dataclasses import dataclass


@dataclass(frozen=True)
class Channel:
    slug: str
    display_name: str
    youtube_url: str
    enabled: bool = True