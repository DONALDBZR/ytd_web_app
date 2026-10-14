from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Resolved_Stream:
    url: str
    mime_type: str
    expires_at: Optional[float]
    title: str