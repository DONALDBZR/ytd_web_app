from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass(frozen=True)
class Resolved_Stream:
    url: str
    mime_type: str
    expires_at: Optional[float]
    title: str
    video_url: Optional[str] = None
    audio_url: Optional[str] = None
    video_headers: Dict[str, str] = field(default_factory=dict)
    audio_headers: Dict[str, str] = field(default_factory=dict)

    @property
    def requires_remux(self) -> bool:
        return bool(self.video_url and self.audio_url)
