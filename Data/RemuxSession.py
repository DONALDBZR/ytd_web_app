from dataclasses import dataclass
from pathlib import Path
from subprocess import Popen


@dataclass
class Remux_Session:
    slug: str
    session_id: str
    directory: Path
    process: Popen
    expires_at: float